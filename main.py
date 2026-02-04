from src.config import TOKEN
from src.bot import AhlwardtBot

if __name__ == "__main__":
    if TOKEN:
        bot = AhlwardtBot()
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN not found in .env")
