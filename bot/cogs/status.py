import discord
from discord import app_commands
from discord.ext import commands
from ..utils.ui import make_embed, COMMANDS

class StatusPanel(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=180)
        self.cog = cog

    @discord.ui.button(label="Statistics", emoji="📊",
                       style=discord.ButtonStyle.primary)
    async def statistics(self, interaction, button):
        await self.cog.show_stats(interaction)

    @discord.ui.button(label="Commands", emoji="📋",
                       style=discord.ButtonStyle.secondary)
    async def command_menu(self, interaction, button):
        await self.cog.show_commands(interaction)

    @discord.ui.button(label="Health", emoji="🏥",
                       style=discord.ButtonStyle.success)
    async def health(self, interaction, button):
        await self.cog.show_health(interaction)

class StatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def show_status(self, interaction):
        users = sum(g.member_count or 0 for g in self.bot.guilds)
        total = await self.bot.db.total()

        e = make_embed(
            "🟢 Bot Status",
            f"**Online**\n{len(self.bot.guilds):,} servers • {users:,} users"
        )
        e.add_field(
            name="⚡ Latency",
            value=f"{self.bot.latency * 1000:.0f}ms",
            inline=True
        )
        e.add_field(
            name="📈 Uptime",
            value=self.bot.metrics.uptime,
            inline=True
        )
        e.add_field(
            name="📋 Commands",
            value=f"{total:,}",
            inline=True
        )
        await interaction.response.send_message(
            embed=e, view=StatusPanel(self.bot.get_cog("StatusCog")),
            ephemeral=True
        )

    async def show_stats(self, interaction):
        users = sum(g.member_count or 0 for g in self.bot.guilds)
        total = await self.bot.db.total()
        rows = await self.bot.db.top()
        top = "\n".join(
            f"`/{name}` — **{uses:,}**" for name, uses in rows
        ) or "No usage yet."

        e = make_embed("📊 Bot Statistics")
        e.add_field(name="Servers", value=f"{len(self.bot.guilds):,}", inline=True)
        e.add_field(name="Users", value=f"{users:,}", inline=True)
        e.add_field(name="Commands", value=f"{total:,}", inline=True)
        e.add_field(name="Most Used", value=top, inline=False)

        await interaction.response.edit_message(
            embed=e, view=StatusPanel(self)
        )

    async def show_commands(self, interaction):
        e = make_embed(
            "📋 Commands",
            "Everything you need, kept simple."
        )
        for name, description in COMMANDS:
            e.add_field(name=name, value=description, inline=False)

        await interaction.response.edit_message(
            embed=e, view=StatusPanel(self)
        )

    async def show_health(self, interaction):
        ms = self.bot.latency * 1000
        assessment = (
            "Excellent" if ms < 100
            else "Good" if ms < 200
            else "Needs Attention"
        )

        e = make_embed("🏥 Bot Health")
        e.add_field(name="Connection", value="🟢 Operational", inline=True)
        e.add_field(name="Latency", value=f"{ms:.0f}ms", inline=True)
        e.add_field(name="Uptime", value=self.bot.metrics.uptime, inline=True)
        e.add_field(name="Assessment", value=f"**{assessment}**", inline=False)

        await interaction.response.edit_message(
            embed=e, view=StatusPanel(self)
        )

    @app_commands.command(name="status", description="Show bot status.")
    async def status(self, interaction):
        await self.bot.db.increment("status")
        await self.show_status(interaction)

    @app_commands.command(name="stats", description="Show bot statistics.")
    async def stats(self, interaction):
        await self.bot.db.increment("stats")
        await interaction.response.defer(ephemeral=True)
        await self.show_stats(interaction)

    @app_commands.command(name="server", description="Show server information.")
    async def server(self, interaction):
        await self.bot.db.increment("server")
        guild = interaction.guild
        e = make_embed("🏠 Server Information")
        e.add_field(name="Name", value=guild.name, inline=True)
        e.add_field(name="Members", value=f"{guild.member_count:,}", inline=True)
        e.add_field(name="Channels", value=f"{len(guild.channels):,}", inline=True)
        e.add_field(name="Roles", value=f"{len(guild.roles):,}", inline=True)
        await interaction.response.send_message(embed=e, ephemeral=True)

    @app_commands.command(name="health", description="Show bot health.")
    async def health(self, interaction):
        await self.bot.db.increment("health")
        await interaction.response.defer(ephemeral=True)
        await self.show_health(interaction)

    @app_commands.command(name="commands", description="Show all bot commands.")
    async def commands_list(self, interaction):
        await self.bot.db.increment("commands")
        await self.show_commands(interaction)

    @app_commands.command(name="settings", description="Show server settings.")
    async def settings(self, interaction):
        await self.bot.db.increment("settings")
        row = await self.bot.db.settings_for(interaction.guild.id)

        e = make_embed("⚙️ Server Settings")
        e.add_field(
            name="Logging",
            value="🟢 Enabled" if row[1] else "🔴 Disabled",
            inline=True
        )
        e.add_field(
            name="Health Reports",
            value="🟢 Enabled" if row[2] else "🔴 Disabled",
            inline=True
        )
        e.add_field(
            name="Welcome",
            value="🟢 Enabled" if row[3] else "🔴 Disabled",
            inline=True
        )
        await interaction.response.send_message(embed=e, ephemeral=True)
