#!/bin/bash
docker compose -f docker-compose-dev.yml run solver python -m pytest --import-mode=importlib -s -x -vv -n logical $*
