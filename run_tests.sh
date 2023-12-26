#!/bin/bash
docker compose -f docker-compose-dev.yml run -v $(pwd):/solver solver python -m pytest -s -x -vv -n logical $*
