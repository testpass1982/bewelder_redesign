#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    DROP DATABASE IF EXISTS bewgb_db;
    DROP USER IF EXISTS bewgb_user;
EOSQL
