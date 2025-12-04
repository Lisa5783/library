#!/bin/bash
echo "Comparing TEST and STAGE schemas..."
diff test_schema.sql stage_schema.sql
