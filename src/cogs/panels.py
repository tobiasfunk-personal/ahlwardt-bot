import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime
from src.utils.helpers import get_target_timezone
from src.utils.traffic import check_traffic_debug

class PanelView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=None) # Persistent view
        self.cog = cog

    @discord.ui.button(label="Place Panel", style=discord.ButtonStyle.primary, emoji="☀️", custom_id="panel_place")
    async def place_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cog.tracking_data["placed"] += 1
        await self.update_message(interaction)
    
    @discord.ui.button(label="Fix Panel", style=discord.ButtonStyle.success, emoji="🔧", custom_id="panel_fix")
    async def fix_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.cog.tracking_data["fixed_this_hour"] += 1
        await self.update_message(interaction)

    async def update_message(self, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        # Update description or fields with new counts
        embed.description = (
            f"**Current Status**\n\n"
            f"☀️ **Placed**: {self.cog.tracking_data['placed']}\n"
            f"🔧 **Fixed (Hour)**: {self.cog.tracking_data['fixed_this_hour']}\n\n"
            f"Use buttons below to update."
        )
        await interaction.response.edit_message(embed=embed)

class Panels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tracking_data = {
            "placed": 0,
            "fixed_this_hour": 0
        }
        self.tracking_message_id = None

    @app_commands.command(name='panels_spawn', description="Spawn the tracking dashboard (Buttons).")
    async def panels_spawn(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Solar Panel Manager", 
            description=f"**Current Status**\n\n☀️ **Placed**: {self.tracking_data['placed']}\n🔧 **Fixed (Hour)**: {self.tracking_data['fixed_this_hour']}\n\nUse buttons below to update.", 
            color=0xFFA500
        )
        
        await interaction.response.send_message(embed=embed, view=PanelView(self))
        msg = await interaction.original_response()
        self.tracking_message_id = msg.id

    @app_commands.command(name='panels_collected', description="Reset 'Placed' count to 0.")
    async def panels_collected(self, interaction: discord.Interaction):
        self.tracking_data["placed"] = 0
        await interaction.response.send_message("✅ Panels collected. Count reset to 0.")

    @app_commands.command(name='panels_status', description="Debug traffic and logic.")
    async def panels_status(self, interaction: discord.Interaction):
        tz = get_target_timezone()
        now = datetime.now(tz)
        present, debug_log = check_traffic_debug(interaction.guild)
        
        status_msg = f"**Status Report**\nTime: {now.strftime('%H:%M:%S')}\nTraffic Present: {present}\n\n**Debug Log**:\n```{debug_log}```"
        await interaction.response.send_message(status_msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Panels(bot))
