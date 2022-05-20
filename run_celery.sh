#!/bin/sh
export DISPLAY=:1
cd gameEngine/runFiles
celery -A runGames worker --loglevel INFO