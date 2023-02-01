import typing

CONFIG_DICT = typing.TypedDict(
    "Config Dict", {"downloadDirectory": str, "maxDownloads": int}
)
