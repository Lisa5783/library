#!/bin/bash
echo "Creating DB backup..."
sqlite3 prod.db ".backup 'backup_$(date +%Y%m%d_%H%M%S).db'"
