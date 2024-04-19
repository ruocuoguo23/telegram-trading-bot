# Binance New Listing Telegram Bot

这个项目包含一个Telegram机器人，用于监控Binance交易所的新币上市信息，并通过Telegram发送通知给订阅用户。

## 功能

- `/start`: 启动机器人并显示欢迎信息。
- `/newlisting`: 订阅Binance新币上市通知。当检测到新币上市时，机器人会发送通知。

## 如何使用

1. 克隆仓库到本地。
2. 安装所需的依赖。
3. 在`config/config.yaml`中配置你的Telegram令牌和其他设置。
4. 运行机器人。

## 安装步骤

确保你已经安装了Python 3.7或更高版本。

1. 克隆仓库：

```bash
git clone git@github.com:ruocuoguo23/telegram-trading-bot.git
cd telegram-trading-bot
```


2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 配置文件：
创建config/config.yaml并填写你的设置。
配置文件config.yaml应该包含以下内容：
```yaml
telegram:
  token: "YOUR_TELEGRAM_BOT_TOKEN"
```

将YOUR_TELEGRAM_BOT_TOKEN替换为你从Telegram BotFather获取的令牌。

4. 运行机器人：
```bash
./start.sh
```

5. 贡献:

如果你想为这个项目贡献代码，请：
Fork这个仓库。
创建一个新的分支。
提交你的更改。
创建一个Pull Request。
