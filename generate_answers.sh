#!/bin/bash
docker compose -f docker-compose-dev.yml run -v $(pwd):/bot bot python -m tests.data.generate_answers $*
