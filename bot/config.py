import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    token: str
    guild_id: int
    database_path: str

token = os.getenv("DISCORD_TOKEN")
guild_id = os.getenv("GUILD_ID")
if not token or not guild_id:
    raise RuntimeError("Set DISCORD_TOKEN and GUILD_ID in .env")

settings = Settings(
    token,
    int(guild_id),
    os.getenv("DATABASE_PATH", "./data/status.db"),
)
