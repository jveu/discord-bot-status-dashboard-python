from pathlib import Path
import aiosqlite

class Database:
    def __init__(self, path):
        self.path = path
        self.db = None

    async def initialize(self):
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.db = await aiosqlite.connect(self.path)
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS usage("
            "command TEXT PRIMARY KEY, uses INTEGER NOT NULL DEFAULT 0)"
        )
        await self.db.execute(
            "CREATE TABLE IF NOT EXISTS settings("
            "guild_id INTEGER PRIMARY KEY, logging INTEGER DEFAULT 1, "
            "health INTEGER DEFAULT 1, welcome INTEGER DEFAULT 0)"
        )
        await self.db.commit()

    async def increment(self, command):
        await self.db.execute(
            "INSERT INTO usage(command,uses) VALUES(?,1) "
            "ON CONFLICT(command) DO UPDATE SET uses=uses+1",
            (command,),
        )
        await self.db.commit()

    async def total(self):
        cur = await self.db.execute(
            "SELECT COALESCE(SUM(uses),0) FROM usage"
        )
        return (await cur.fetchone())[0]

    async def top(self):
        cur = await self.db.execute(
            "SELECT command,uses FROM usage ORDER BY uses DESC LIMIT 8"
        )
        return await cur.fetchall()

    async def settings_for(self, guild_id):
        cur = await self.db.execute(
            "SELECT guild_id,logging,health,welcome FROM settings "
            "WHERE guild_id=?", (guild_id,)
        )
        row = await cur.fetchone()
        if row:
            return row
        await self.db.execute(
            "INSERT INTO settings(guild_id) VALUES(?)", (guild_id,)
        )
        await self.db.commit()
        return (guild_id, 1, 1, 0)

    async def close(self):
        if self.db:
            await self.db.close()
