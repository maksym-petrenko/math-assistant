#!/bin/bash
docker compose run -v $(pwd)/tests:/bot/tests bot python -m pytest -s -x -n logical $*
