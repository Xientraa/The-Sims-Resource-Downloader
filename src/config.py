import json, typing
from pathlib import Path
from platformdirs import user_config_dir, user_state_dir, user_downloads_dir

# Paths
APP_AUTHOR = "Xientraa"
APP_NAME = "TSR-Downloader"

CONFIG_DIR = Path(user_config_dir(APP_NAME, APP_AUTHOR))
STATE_DIR = Path(user_state_dir(APP_NAME, APP_AUTHOR))
DOWNLOADS_DIR = Path(user_downloads_dir()) / APP_NAME

for dir in [CONFIG_DIR, STATE_DIR, DOWNLOADS_DIR]:
    dir.mkdir(parents=True, exist_ok=True)


# Config
class ConfigDict(typing.TypedDict):
    downloadDirectory: str
    maxActiveDownloads: int
    saveDownloadQueue: bool
    debug: bool


DEFAULT_CONFIG: ConfigDict = {
    "downloadDirectory": str(DOWNLOADS_DIR),
    "maxActiveDownloads": 4,
    "saveDownloadQueue": True,
    "debug": False,
}

CONFIG_FILE = CONFIG_DIR / "config.json"
if not CONFIG_FILE.exists():
    CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))

CONFIG = json.loads(CONFIG_FILE.read_text())
