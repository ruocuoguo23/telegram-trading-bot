# Binance New Listing Telegram Bot

This project includes a Telegram bot that monitors new cryptocurrency listings on the Binance exchange and sends notifications to subscribed users via Telegram.

## Features

- `/start`: Launches the bot and displays a welcome message.
- `/newlisting`: Subscribes to notifications of new listings on Binance. When a new listing is detected, the bot sends out a notification.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies.
3. Configure your Telegram token and other settings in `config/config.yaml`.
4. Run the bot.

## Installation Steps

Make sure you have Python 3.7 or higher installed.

1. Clone the repository:

    ```bash
    git clone git@github.com:ruocuoguo23/telegram-trading-bot.git
    cd telegram-trading-bot
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Configuration file:
Create config/config.yaml and fill in your settings.
The config.yaml file should contain the following:
    ```yaml
    telegram:
      token: "YOUR_TELEGRAM_BOT_TOKEN"
    ```

    Replace YOUR_TELEGRAM_BOT_TOKEN with the token you obtained from Telegram's BotFather.

4. Run the bot:
    ```bash
    ./start.sh
    ```

5. Contributing:
If you would like to contribute to this project, please:

    Fork the repository.
    Create a new branch.
    Submit your changes.
    Create a Pull Request.