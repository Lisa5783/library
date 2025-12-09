#!/bin/bash
set -e

echo "Running SQL security & lint check..."

# если у тебя Postgres:
sqlfluff lint db_schema/*.sql --dialect postgres

