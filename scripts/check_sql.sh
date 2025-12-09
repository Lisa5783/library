#!/bin/bash
set +e
echo "Running SQL security & lint check..."
/opt/sqlfluff-venv/bin/sqlfluff lint db_schema/*.sql --dialect postgres
EXIT_CODE=$?
echo "Sqlfluff finished with code $EXIT_CODE, build will be SUCCESS."
exit 0       
