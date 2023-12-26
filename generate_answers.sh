#!/bin/bash
docker compose -f docker-compose-dev.yml run solver python -m solver.tests.generate_answers $*
