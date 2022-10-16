import dbm
import json
from pathlib import Path

from asgiref.sync import sync_to_async
from box import Box

from . import log

def load_settings(app):
    """Return a dictionary of settings from the settings database."""
    path = app.config["settings_path"]
    if not path.exists():
        return {}
    settings = {}
    with dbm.open(str(path), 'c') as db:
        for key in db.keys():
            log.debug("Load: ", key, db[key])
            settings[key.decode('utf-8')] = json.loads(db[key].decode('utf-8'))  # type: ignore
    return Box(settings)

def save_settings(app):
    """Save the settings to the settings database."""
    path = app.config["settings_path"]
    settings = app.config["settings"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with dbm.open(str(path), 'c') as db:
        for key, value in settings.items():
            log.debug("Save: ", key, value)
            db[key.encode('utf-8')] = json.dumps(value).encode('utf-8')

@sync_to_async
def update_setting(app, key, value):
    """Update a single setting in the settings database."""
    path = app.config["settings_path"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with dbm.open(str(path), 'c') as db:
        log.debug("Update: ", key, value)
        db[key.encode('utf-8')] = json.dumps(value).encode('utf-8')