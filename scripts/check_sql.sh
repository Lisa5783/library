#!/bin/bash
echo "Running SQL security & lint check..."
sqlfluff lint db_schema/*.sql
