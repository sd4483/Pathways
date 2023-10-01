# Pathways Sandbox
 
1. Download the .zip file and extract it
2. Setup a new python virtual environment on your machine
3. Activate the environment
4. If you are running Ubuntu or Ubuntu based OS, you need to install libpq-dev for
psycopg-2 to install properly. You can install it using
    sudo apt-get install libpq-dev
5. Install all the dependencies listed in the requirements.txt file using pip.
6. Setup a new PostgreSQL database and update the database configuration in Set- tings.py file
7. After installing everything, cd into the app directory where manage.py file is located and run these commands sequentially
    python manage.py migrate
    python manage.py collectstatic
    python manage.py runserver
8. If everything is setup properly, the server should be running on your localhost.
