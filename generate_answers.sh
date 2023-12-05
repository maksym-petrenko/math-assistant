#!/bin/bash
docker compose run -v $(pwd)/tests:/bot/tests bot python -m tests.data.generate_answers $*
