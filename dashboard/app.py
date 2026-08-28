from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="Discord Bot Status Dashboard")

@app.get("/", response_class=HTMLResponse)
async def home():
    return '''
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Discord Bot Status</title>
<style>
body{font-family:system-ui;background:#0f1117;color:#fff;max-width:850px;
margin:60px auto;padding:20px}
.card{background:#181b24;border:1px solid #292e3a;border-radius:18px;padding:28px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.stat{background:#11141b;padding:18px;border-radius:14px}
.muted{color:#9299a8}.ok{color:#55d98a}
</style>
</head>
<body>
<div class="card">
<h1>Discord Bot Status</h1>
<p class="ok">● Online</p>
<div class="grid">
<div class="stat"><span class="muted">Servers</span><h2>—</h2></div>
<div class="stat"><span class="muted">Users</span><h2>—</h2></div>
<div class="stat"><span class="muted">Uptime</span><h2>—</h2></div>
</div>
<p class="muted">Starter dashboard — connect this page to the bot API for live metrics.</p>
</div>
</body>
</html>
'''
