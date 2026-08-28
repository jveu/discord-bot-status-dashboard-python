# Discord Bot Status Dashboard

A clean, simple Python Discord bot for status, statistics, health, server information, settings, and commands.

**MESSAGE @JVEU ON DISCORD IF WANTING ANY PERMISIONS TO SELL ETC**

**Credits: @jveu**

## Commands
- `/status` — Bot status, latency, uptime and totals
- `/stats` — Servers, users and command usage
- `/server` — Current server information
- `/health` — Compact bot health report
- `/commands` — Clean command list
- `/settings` — Server configuration

The Discord UI uses compact embeds and interactive buttons.

## Setup
1. Install Python 3.10+
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`
4. Add your bot token and test guild ID
5. Run `python -m bot`

Optional web dashboard:
`uvicorn dashboard.app:app --reload`

See `LICENSE` for usage and redistribution restrictions.
