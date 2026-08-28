import discord

COMMANDS = [
    ("`/status`", "View bot status, latency and uptime."),
    ("`/stats`", "View servers, users and command statistics."),
    ("`/server`", "View this server's information."),
    ("`/health`", "View a compact health report."),
    ("`/commands`", "View the command list."),
    ("`/settings`", "View server configuration."),
]

def make_embed(title, description=None):
    return discord.Embed(
        title=title,
        description=description,
        color=discord.Color.blurple()
    )
