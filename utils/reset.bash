while true
do
    echo "0 - Make all operations"
    echo "1 - Remove migrations"
    echo "2 - Make migrations"
    echo "3 - Apply migrations"
    echo "4 - Fill DB"
    echo "Any other key to exit"

    read -p "Choose action > " choice
    case "$choice" in
        0 )
            bash utils/remove_migrations.bash
            python manage.py makemigrations
            python manage.py migrate
            python manage.py mommy_fill_db
        ;;
        1 ) bash utils/remove_migrations.bash;;
        2 ) python manage.py makemigrations;;
        3 ) python manage.py migrate;;
        4 ) python manage.py mommy_fill_db;;
        * ) break;;
    esac
done
