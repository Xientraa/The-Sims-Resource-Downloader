#!/bin/bash

DIR="$( dirname -- "$0" )"
DIR="$( realpath -e  -- "$DIR"; )"
cd "$DIR"

if ! type "python" > /dev/null; then
    echo "Python is not installed, please install python using your package manager and try again."
    exit
fi

if [ ! -d "./env" ]; then
    echo "Python environment doesn't exist, creating python environment."
    python -m venv ./env
fi

source ./env/bin/activate

if type "pip" > /dev/null; then
    ./env/bin/pip install -qr ./requirements.txt
else
    echo "Cannot find pip, please install pip and try again."
    exit
fi

./env/bin/python ./src/main.py
