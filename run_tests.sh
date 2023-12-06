#!/bin/bash
docker compose run -v $(pwd):/bot bot python -m pytest -s -x -n logical $*
