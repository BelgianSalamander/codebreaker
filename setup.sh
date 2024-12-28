#!/bin/sh

mkdir -p temp/
sqlite3 codebreaker.db < table_setup.sql
