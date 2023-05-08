import json, os, typing

CONFIG_DICT = typing.TypedDict(
    "Config Dict",
    {
        "downloadDirectory": str,
        "maxActiveDownloads": int,
        "saveDownloadQueue": bool,
        "debug": bool,
    },
)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG: CONFIG_DICT = json.load(open(CURRENT_DIR + "/config.json", "r"))
