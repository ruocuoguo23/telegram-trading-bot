import re
import requests
from requests.adapters import HTTPAdapter
from typing import Optional
from bs4 import BeautifulSoup
import json
import time
import random

from utils import trading_logger


class HostHeaderSSLAdapter(HTTPAdapter):
    def send(self, request, **kwargs):
        # HTTP headers are case-insensitive (RFC 7230)
        host_header = None
        for header in request.headers:
            if header.lower() == "host":
                host_header = request.headers[header]
                break

        connection_pool_kwargs = self.poolmanager.connection_pool_kw

        if host_header:
            connection_pool_kwargs["assert_hostname"] = host_header
            connection_pool_kwargs["server_hostname"] = host_header
        elif "assert_hostname" in connection_pool_kwargs:
            # an assert_hostname from a previous request may have been left
            connection_pool_kwargs.pop("assert_hostname", None)
            connection_pool_kwargs.pop("server_hostname", None)

        return super(HostHeaderSSLAdapter, self).send(request, **kwargs)


class NewListingContent:
    def __init__(self, title, release_date, code):
        self.title = title
        self.release_date = release_date
        self.code = code

        self.symbol = None

    def __str__(self):
        return f"title: {self.title}, release date: {self.release_date}, code: {self.code}, symbol: {self.symbol}"


class BinanceListingChecker:
    def __init__(self):
        self.ip_list = [
            '52.84.150.52',
            '52.84.150.48',
            '52.84.150.36',
            '52.84.150.65',
        ]
        # self.binance_url = "https://www.binance.com/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"
        # self.binance_url = f"https://{self.ip}/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 '
            'Safari/537.3',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 '
            'Safari/537.36 Edg/89.0.774.57',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
            'Version/14.0.3 Mobile/15E148 Safari/604.1',
        ]

        self.headers = {
            'Host': 'www.binance.com'
        }
        self.session = requests.Session()
        binance_adapter = HostHeaderSSLAdapter(pool_connections=1, pool_maxsize=1)
        self.session.mount('https://', binance_adapter)

        self.latest_code = None
        self.latest_release_date = None

        self.retry_interval = 10

    def initialize(self):
        # we get the first announcement and set it as the latest announcement
        try:
            first_article = self.get_first_article()
            self.latest_code = first_article['code']
            self.latest_release_date = first_article['releaseDate']

            trading_logger.info(f"Initialize BinanceListingChecker with latest code: {self.latest_code}, "
                                f"latest title: {first_article['title']}")

            return True
        except Exception as e:
            trading_logger.error(f"Error while initialize BinanceListingChecker: {e}")
            return False

    def get_random_ip_url(self):
        ip = random.choice(self.ip_list)
        url = f"https://{ip}/en/support/announcement/new-cryptocurrency-listing?c=48&navId=48"

        return ip, url

    def get_random_user_agent(self):
        return random.choice(self.user_agent_list)

    def check(self):
        """
        Checks if there is a new listing announcement. If there is, return NewListingContent object with token symbol.
        """
        try:
            first_article = self.get_first_article()
            lastest_title = first_article['title']
            article_release_timestamp = first_article['releaseDate']
            code = first_article['code']

            if code == self.latest_code:
                return None

            if article_release_timestamp < self.latest_release_date:
                return None

            # update latest announcement info
            self.latest_release_date = article_release_timestamp
            self.latest_code = code

            trading_logger.info(f"New announcement: {lastest_title}, "
                                f"code: {code}, release date: {article_release_timestamp}")

            content = NewListingContent(lastest_title, article_release_timestamp, code)
            content.symbol = BinanceListingChecker.get_listing_symbol(lastest_title)
            # article_release_timestamp is in milliseconds since epoch
            return content

        except Exception as e:
            trading_logger.error(f"Error while checking binance announcement: {e}")
            return None

    def scrap(self, url) -> Optional[BeautifulSoup]:
        try:
            # get random user agent
            user_agent = self.get_random_user_agent()
            self.headers['User-Agent'] = user_agent

            # reuse the session
            response = self.session.get(url, headers=self.headers)

            if response.status_code == 200:
                return BeautifulSoup(response.text, 'html.parser')

            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            trading_logger.error(f"HTTP error occurred: {http_err}")

            if http_err.response.status_code == 429:
                trading_logger.error(f"Response headers: {http_err.response.headers}")
                trading_logger.error(f"Response body: {http_err.response.text}")
                trading_logger.error(f"Too many requests, sleep 10 seconds")

                time.sleep(self.retry_interval)
        except requests.exceptions.ConnectionError as conn_err:
            trading_logger.error(f"Connection error occurred: {conn_err}")
        except requests.exceptions.Timeout as timeout_err:
            trading_logger.error(f"Timeout error occurred: {timeout_err}")
        except requests.exceptions.RequestException as req_err:
            trading_logger.error(f"General Request exception: {req_err}")
        except Exception as e:
            trading_logger.error(f"An error occurred: {e}")
        finally:
            self.session.cookies.clear()

        return None

    @staticmethod
    def get_script_data(soup):
        return soup.find('script', {'id': '__APP_DATA'})

    def get_first_article(self):
        # first get ip and url to use
        ip, url = self.get_random_ip_url()

        scrap_result = self.scrap(url)
        if not scrap_result:
            raise Exception("Scrap failed, maybe too many requests or connection error")
        else:
            script_data = scrap_result.find('script', {'id': '__APP_DATA'})
            return BinanceListingChecker.get_articles(script_data)[0]

    @staticmethod
    def get_articles(script_data):
        json_data = json.loads(script_data.contents[0])
        app_state = json_data.get('appState', {})
        articles = app_state.get('loader', {}).get('dataByRouteId', {}).get('d9b2', {}).get('catalogs', [])[0].get(
            'articles', [])
        return articles

    @staticmethod
    def get_listing_symbol(title: str) -> str:
        # first if the title is a listing announcement, for example:
        # Binance Will List Bonk (BONK) with Seed Tag Applied
        list_prefix = "Binance Will List"
        if title.startswith(list_prefix):
            # try to get the symbol
            match = re.search(r'\((.*?)\)', title)
            if match:
                return match.group(1)

        return ""
