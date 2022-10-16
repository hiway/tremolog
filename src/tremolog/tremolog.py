import asyncio
from pathlib import Path

from click import get_app_dir
from quart import Quart, render_template
from quart_cors import cors

from . import log
from .settings import load_settings, save_settings, update_setting

app = Quart(__name__)
app = cors(app)
app.config["app_dir"] = Path(get_app_dir("tremolog"))
app.config["settings_path"] = app.config["app_dir"] / "settings.db"
app.config["settings"] = load_settings(app)


@app.before_serving
async def load_settings_before_serving():
    if not app.config["settings"].get("counter"):
        app.config["settings"]["counter"] = 0


@app.after_serving
async def save_settings_after_serving():
    save_settings(app)


@app.route("/")
async def index():
    log.info(f"Rendering index.html")
    app.config["settings"]["counter"] += 1
    counter = app.config["settings"]["counter"]
    asyncio.ensure_future(update_setting(app, "counter", counter))  # Save in background
    return await render_template("index.html", counter=counter)
