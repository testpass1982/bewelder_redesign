#!/usr/bin/env bash

# Try 'utils/reset.sh' to run.
# 'utils/reset.sh OPTION[0..6]' to run with preselected option and exit.

if [[ $0 != "utils/reset.sh" ]]; then
    echo "Try 'utils/reset.sh'"
    exit
fi

if [ -n "$1" ]; then
    CHOICE=$1
fi

chmod +x utils/*

while true
do
    if [ -z "$1" ]; then
        echo "Enter 'help' for show legend"
        read -p "Choose action > " CHOICE
    fi
    case "$CHOICE" in
        "help" )
                echo "0 - Make all operations"
                echo "1 - Drop DB"
                echo "2 - Create DB"
                echo "3 - Remove migrations"
                echo "4 - Make migrations"
                echo "5 - Apply migrations"
                echo "6 - Fill DB"
                echo "Any other key to exit"
        ;;
        0 )
            utils/postgres_db_drop.sh
            utils/postgres_db_create.sh
            utils/remove_migrations.sh
            python manage.py makemigrations
            python manage.py migrate
            python manage.py mommy_fill_db
            break
        ;;
        1 ) utils/postgres_db_drop.sh;;
        2 ) utils/postgres_db_create.sh;;
        3 ) utils/remove_migrations.sh;;
        4 ) python manage.py makemigrations;;
        5 ) python manage.py migrate;;
        6 ) python manage.py mommy_fill_db;;
        * ) break;;
    esac
    if [ -n "$1" ]; then
        break
    fi
done
