# The Sims Resource Downloader

[![Code Style: Black](https://img.shields.io/badge/Code_Style-Black-black.svg?style=for-the-badge)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/github/license/Xientraa/The-Sims-Resource-Downloader?label=License&style=for-the-badge)](./LICENSE)

I created this tool because I found it infuriating to download stuff from The Sims Resource, their 15 second wait along with only being able to download a single item at a time and them plastering advertisements everywhere for their VIP service.

With this tool you can download multiple items at once, to download items copy the url of the item, the tool monitors your clipboard for valid URLs to download from, and will automatically start downloading the item to the supplied directory in the `config.json` file.

For a fully in-depth guide of how to setup and use this tool, check out the [Wiki](https://github.com/Xientraa/The-Sims-Resource-Downloader/wiki).

## Configuration

| Option | Description | type |
| - | - | - |
| downloadDirectory | Path to a directory where the files will be downloaded to. | string |
| maxActiveDownloads | Limits the amount of concurrent downloads. | integer |
| saveDownloadQueue | Toggles saving & loading of active downloads & queued downloads. | boolean |
| debug | Toggles debug messages from the logger. | boolean |

## Setting Up Environment

```sh
python -m venv ./env/
```

## Installing Requirements

```pip
pip install -r requirements.txt
```

## Usage

```sh
python src/main.py
```
