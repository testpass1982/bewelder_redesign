sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE bewgb_db;
    CREATE USER bewgb_user WITH PASSWORD 'password';
    ALTER ROLE bewgb_user SET client_encoding TO 'utf8';
    ALTER ROLE bewgb_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE bewgb_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE bewgb_db TO bewgb_user;
    ALTER USER bewgb_user CREATEDB;
EOSQL
