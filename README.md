# Telegram bot for downloading music from Soundcloud/Youtube (mp3 format)


> [!WARNING]
> The bot is still rough around the edges; recommend reviewing the code before running it. I am not responsible for your actions


## Usage
1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh`
2. Clone git repo: git clone `https://github.com/wmord/tg-bot-yt.sc.downloader`
3. Edit 13 string in main.py (list of people who will have access to the bot's functionality). Past your UID 
4. In cloned directory launch: `TOKEN=YOUR_BOT_TOKEN uv run main.py`

## How to get bot token?
1. Start bot **@BotFather** in Telegram
2. Type **/newbot** and follow the instructions
3. Copy the line following _"Use this token to access the HTTP API:"_, it's your bot token

## Where can i find my UID?
In the bot **@username_to_id_bot** in telegram

[If this project helped you](https://github.com/wmord/wmord/blob/main/sup.md)
