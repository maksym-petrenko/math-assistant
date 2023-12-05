#!/bin/bash
docker compose run bot python -m pytest -s -x $*
