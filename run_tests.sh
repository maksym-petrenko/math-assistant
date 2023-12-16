#!/bin/bash
docker compose -f docker-compose-dev.yml run -v $(pwd):/bot bot python -m pytest -s -x -vv -n logical $*
