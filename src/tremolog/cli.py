import click
from click import get_app_dir
from pathlib import Path
from quart import Quart

from .settings import load_settings, save_settings


@click.group()
def main():
    pass


@main.command()
@click.option("--api-id", prompt="Telegram API ID", help="Telegram API ID")
@click.option("--api-hash", prompt="Telegram API Hash", help="Telegram API Hash")
@click.option("--bot-token", prompt="Telegram Bot Token", help="Telegram Bot Token")
@click.option("--bot-admin", prompt="Telegram Bot Admin", help="Telegram Bot Admin")
def login(api_id, api_hash, bot_token, bot_admin):
    """Configure Telegram login"""
    app = Quart(__name__)
    app.config["app_dir"] = Path(get_app_dir("tremolog"))
    app.config["settings_path"] = app.config["app_dir"] / "settings.db"
    app.config["settings"] = load_settings(app)
    app.config["settings"]["telegram"] = {
        "api_id": api_id,
        "api_hash": api_hash,
        "bot_token": bot_token,
        "bot_admin": bot_admin,
    }
    save_settings(app)
    click.echo("Telegram login configured")


if __name__ == "__main__":
    main()
