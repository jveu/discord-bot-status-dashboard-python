import time

class Metrics:
    def __init__(self):
        self.started = time.monotonic()

    @property
    def uptime(self):
        seconds = int(time.monotonic() - self.started)
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        parts = []
        if days: parts.append(f"{days}d")
        if hours: parts.append(f"{hours}h")
        if minutes: parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        return " ".join(parts)
