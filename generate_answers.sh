#!/bin/bash
docker compose run -v $(pwd):/bot bot python -m tests.data.generate_answers $*
