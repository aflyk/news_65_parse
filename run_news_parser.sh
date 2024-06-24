#!/bin/sh

poetry shell
python process_run_parsing.py
exec "$@"
