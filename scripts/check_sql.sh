#!/bin/bash
set -e

echo "Running SQL security & lint check..."

# используем sqlfluff из venv, который мы поставили в шаге Install Sqlfluff
/opt/sqlfluff-venv/bin/sqlfluff lint db_schema/*.sql --dialect postgres
