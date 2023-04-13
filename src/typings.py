import typing

CONFIG_DICT = typing.TypedDict(
    "Config Dict", {"downloadDirectory": str, "maxActiveDownloads": int}
)
