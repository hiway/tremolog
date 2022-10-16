import asyncio
from pathlib import Path

import pytz
from click import get_app_dir
from quart import Quart, render_template
from quart_cors import cors

from . import log
from .models import init, Posts
from .settings import load_settings, save_settings, update_setting
from .telegram import TelegramAgent

app = Quart(__name__)
app = cors(app)
app.config["app_dir"] = Path(get_app_dir("tremolog"))
app.config["settings_path"] = app.config["app_dir"] / "settings.db"
app.config["database_path"] = app.config["app_dir"] / "tremolog.db"
app.config["settings"] = load_settings(app)
app.jinja_options["extensions"] = ["jinja2_humanize_extension.HumanizeExtension"]


telegram = None


@app.before_serving
async def load_settings_before_serving():
    await init(f"sqlite://{app.config['database_path']}")
    print(f"Database initialized at {app.config['database_path']}")
    posts = await Posts.all()
    print(posts)
    if not app.config["settings"].get("counter"):
        app.config["settings"]["counter"] = 0
    if app.config["settings"].get("telegram"):
        api_id = app.config["settings"]["telegram"]["api_id"]
        api_hash = app.config["settings"]["telegram"]["api_hash"]
        bot_token = app.config["settings"]["telegram"]["bot_token"]
        bot_admin = app.config["settings"]["telegram"]["bot_admin"]
        work_dir = app.config["app_dir"]
        global telegram
        telegram = TelegramAgent("tremolog", bot_admin, work_dir)
        await telegram.connect(api_id, api_hash, bot_token)
    else:
        log.error("No Telegram settings found, configure with: $ tremolog login")


@app.after_serving
async def save_settings_after_serving():
    save_settings(app)


@app.route("/")
async def index():
    log.info(f"Rendering index.html")
    app.config["settings"]["counter"] += 1
    counter = app.config["settings"]["counter"]
    asyncio.ensure_future(update_setting(app, "counter", counter))  # Save in background
    posts = await Posts.all().order_by("-created_at").limit(10)
    return await render_template("index.html", counter=counter, posts=posts, pytz=pytz)
