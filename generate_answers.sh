#!/bin/bash
docker compose run -v $(pwd)/tests/data:/bot/tests/data bot python -m tests.data.generate_answers $*
