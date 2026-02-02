# Setup Guide for Knecht Ahlwardt Bot

## 1. Wispbyte (or generic Host) Setup
The project files are ready to be uploaded.
1. Upload `main.py`, `requirements.txt`.
2. **Startup Command**: Set to `python main.py`.
3. **Dependencies**: Wispbyte should auto-install from `requirements.txt`.

## 2. Configuration (Environment Variables)
You need to set these "Secrets" or "Environment Variables" in your hosting panel (or `.env` file for local testing).

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DISCORD_TOKEN` | Your Bot Token from Discord Developer Portal | `MTA...` |
| `TARGET_GUILD_ID` | Right-click Server Icon -> Copy ID | `123456789...` |
| `TARGET_CHANNEL_ID` | Right-click the Channel for pings -> Copy ID | `987654321...` |
| `TARGET_ROLE_NAME` | Exact name of the role to ping | `Ahlwardt` |
| `TARGET_GAME_NAME` | Exact name of the game (Activity) to filter traffic | `Solar Panel Simulator` |
| `TIMEZONE` | Your timezone (important for 04:00 reset) | `Europe/Berlin` |

> [!TIP]
> To get IDs, enable "Developer Mode" in Discord: User Settings > Advanced > Developer Mode.

## 3. Usage
1. **Start**: In the channel, type `/panels_spawn`.
   - The bot will post the tracking embed and add ☀️ and 🔧.
2. **Placing**: Users click ☀️.
3. **Fixing**: Users click 🔧.
   - If fixed (🔧 count > 1), the bot stays silent at XX:31.
   - At XX:30 (next hour), the bot removes user 🔧 reactions automatically.
4. **Reseting**: When confirmed finished/collected, type `/panels_collected`.

## 4. Traffic Awareness Check
The bot strictly checks:
- Is member in Role "Ahlwardt"?
- Is member Status NOT Offline?
- Is member Activity Name == `TARGET_GAME_NAME`? (Make sure this matches exactly what Discord shows under "Playing ...")
