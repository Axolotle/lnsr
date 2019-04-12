#!/usr/bin/env bash

python generate.py

inotifywait --quiet --recursive --monitor --event modify --format "%w%f" . \
| while read change; do
    clear
    python generate.py
    xdotool search --name 'Light-nanosecond' key F5
done
