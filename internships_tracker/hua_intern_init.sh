#!/bin/bash
checkdb=$(nc -zv db 5432 2>&1)
echo $checkdb
while [[ $checkdb == *'failed'* ]]
do
  echo 'Waiting for data base to connect...'
  sleep 1
  checkdb=$(nc -zv db 5432 2>&1)
done

# Make migrations if required
if [ $MAKE_MIGRATIONS = "True" ]; then
  echo "Making migrations..."
  python3 /appinternships/manage.py makemigrations
fi

if [ $MIGRATE = "True" ]; then
  echo "Migrating database..."
  python3 /appinternships/manage.py migrate
fi

if [ $COLLECT_STATIC = "True" ]; then
  echo "Collecting static files..."
  python3 /appinternships/manage.py collectstatic --no-input
fi


#Does a superuser need to be created?
echo "Checking for existent superuser"
if [ $SUPERUSER = "False" ]; then
  echo "Creating superuser..."
  python3 /appinternships/manage.py createsuperuser --noinput
fi

# start development server
python3 /appinternships/manage.py runserver 0.0.0.0:8000