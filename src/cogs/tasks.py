import discord
from discord.ext import commands, tasks
from datetime import datetime
from src.utils.helpers import get_target_timezone
from src.utils.traffic import check_traffic_debug
from src.config import TARGET_CHANNEL_ID, TARGET_ROLE_NAME

class BackgroundTasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_checked_minute = -1

    async def cog_load(self):
        self.check_time.start()

    async def cog_unload(self):
        self.check_time.cancel()

    @tasks.loop(seconds=45)
    async def check_time(self):
        target_channel = self.bot.get_channel(TARGET_CHANNEL_ID)
        if not target_channel:
            return

        tz = get_target_timezone()
        now = datetime.now(tz)
        
        if now.minute == self.last_checked_minute:
            return
        self.last_checked_minute = now.minute

        # Get Panels cog for state
        panels_cog = self.bot.get_cog("Panels")
        if not panels_cog:
            print("Warning: Panels cog not found. Skipping logic involving state.")
            return
        
        # Logic Implementation
        
        # 04:00 - Hard Reset
        if now.hour == 4 and now.minute == 0:
            panels_cog.tracking_data["placed"] = 0
            panels_cog.tracking_data["fixed_this_hour"] = 0
            await target_channel.send("ℹ️ Server Restart: Panel tracking reset.")
            return

        # XX:30 - Reset "Fixed" status for hour
        if now.minute == 30:
            if panels_cog.tracking_data["fixed_this_hour"] > 0:
                panels_cog.tracking_data["fixed_this_hour"] = 0
            return

        # Reminders: XX:31, XX:45, XX:50, XX:55
        if now.minute in [31, 45, 50, 55]:
            # Check Traffic
            traffic_present, _ = check_traffic_debug(target_channel.guild)
            if not traffic_present:
                return

            # Check Logic
            if panels_cog.tracking_data["placed"] > 0 and panels_cog.tracking_data["fixed_this_hour"] == 0:
                role = discord.utils.get(target_channel.guild.roles, name=TARGET_ROLE_NAME)
                mention = role.mention if role else "@here"
                await target_channel.send(f"⚠️ {mention} Panels placed but not fixed! (Time: {now.strftime('%H:%M')})")

    @check_time.before_loop
    async def before_check_time(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(BackgroundTasks(bot))
