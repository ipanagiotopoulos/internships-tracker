## **Hi there 👋**

# Harokopio Univeristy Internships Tracker

Internships tracker is a Django Web application implemented in order to track the progress of internships at the [Harokopio Univeristy of Athens](https://hua.gr)


This system appeals to Public and Private Sector Carriers who want to participate in Harokopio University's Internships Programm.

This application provides a means of communication between students, professors, carriers and the secretary of the univeristy upon intrnships'
matters.

**This project is my thesis work for the B.sc in the Department of Informatics and Telematics at the Harokopio University of Athens.**


## Prerequisites
You should have [**Docker**](https://docker.io)  installed in your local machine and [**docker-compose**](https://docs.docker.com/compose/).

## Helpful extra software
**For dev purposes:**

A fully setup [**Python environment**](https://docs.python.org/3/tutorial/venv.html) will help.
But our environment is fully containarized, so it is not a must.

You can also use the package manager [pip](https://pip.pypa.io/en/stable/) if you want to experiment with this repo in you host machine .



## Installation

Install  [**Docker**](https://docker.io) in your local machine and [**docker-compose**](https://docs.docker.com/compose/) if you don't have it already.

**Clone repository**
git clone https://github.com/ipanagiotopoulos/InternshipsTracker


## Usage

**Workspace** is located under **InternshipsApp** folder.

This stack contains three different containers

```docker-compose
version: "3.7"
services:
  db:
    image: postgres
    container_name: internships_db
    restart: always
    environment:
      - POSTGRES_HOST=db
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=admin
    volumes:
      - ../data/db:/var/lib/postgresql/data;
    ports:
      - "5432:5432"
  web:
    build: .
    container_name: internships_web
    env_file:
      - ./internships_tracker/.env
    ports:
      - 8000:8000
    volumes:
      - ./internships_tracker:/appinternships
      - ../logs:/var/log
    depends_on:
      - db
  nginx:
    image: nginx
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/static:/var/www/static/html
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - web
volumes:
  static_volume: null
```

## internships_db 
**internships_db** container is based on a postresql image which is responsible for persisting the DBMS system in our application
     
## internships_web 
**internships_web** is an ubuntu container where we run our Django web application

In this container we mainly use the below volumes:
   
   **./internships_tracker:/appinternships** a live volume which is used to make changes in our code base and laod them  to the WSGI server in this    container.


  **../logs:/var/log** keeps operating system logs(Ubuntu container) in case you log in into the container and execute some maintenance jobs
 
 This container is being build upon this DockerFile
 
```Dokcerfile
   # Docker file for building the required system starting from Ubuntu 20.04 image
   FROM ubuntu:20.04
   ARG DEBIAN_FRONTEND=noninteractive
   RUN apt-get update && apt-get install -y curl apt-utils apt-transport-https debconf-utils \
       gcc build-essential libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils python3-pip \
       netcat net-tools  libpq-dev

   # set environment variables
   ENV PYTHONDONTWRITEBYTECODE 1
   ENV PYTHONUNBUFFERED 1
   WORKDIR /appinternships
   ENV PATH=$PATH:/appinternships/.local/bin
   COPY requirements.txt /reqs/
   RUN pip install -r /reqs/requirements.txt
   RUN pip install django-phonenumber-field[phonenumbers]
   COPY ./internships_tracker /appinternships
   RUN chmod +x /appinternships/hua_intern_init.sh
   CMD /appinternships/hua_intern_init.sh
 ```
 
 The most import details of this dockerfile are the last 6 steps.
 
  **1.COPY requirements.txt /reqs/**

 Copy the requirements in order to install all our dependencies in the python environment.
 
 **2.RUN pip install -r /reqs/requirements.txt**
 
 All our requirements are being installed in the container.
 
 **3.RUN pip install django-phonenumber-field[phonenumbers]**
 
 django-phonenumber is a special dependency for mobile phone validation which we use in our Django application.
 
 **4.COPY ./internships_tracker /appinternships**
 
 Copy the workspace of our django project to the container.

 **5.RUN chmod +x /appinternships/hua_intern_init.sh**
 
  Give permission to run our script into the container. 
  
  **6.CMD /appinternships/hua_intern_init.sh**
  
  Execute the script in order to run the stack with our migrations.

**hua_intern_init.sh** is an essential script which has been built in order to run our stack without having any problems.

We have a set of checks before running our WSGI server in this container.

```hua_intern_init.sh
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
 ```
 
We are initially checking if the db port is open to connection in this section:
  
 ```
  while [[ $checkdb == *'failed'* ]]
   do
     echo 'Waiting for data base to connect...'
     sleep 1
     checkdb=$(nc -zv db 5432 2>&1)
   done
   
  ```
  
  Also in order to execute this script we must set the according value to our env variables located in the **.env** file:
  
  More specifically:
  ``` $SUPERUSER ``` must be set to  ``` false ``` in order to create an admin by our django-admin.
  
  

  When  ``` $MAKE_MIGRATIONS ``` is set to  ``` false ``` then all migrations from our django apps'  models are being created.

  Otherwise we skip the migrations' creation part.


  
  When  ``` $MIGRATIONS ``` is set to  ``` true ``` then all migrations from our django apps'  models are executed.

  Otherwise we rely on migrations that are already loaded in the volume
  
  
 ``` $COLLECT_STATIC ``` must be set to  ``` true ```  because all static files are preloaded.
    
  **In case**  there is a problem while trying to load static files se this env variable to  ``` true ```

  
  
## nginx 
**nginx** container serves as a reverse proxy for accessing content from our django application
 In nginx container we mainly use the below volumes:
 
  **/nginx/static:/var/www/static/html** a volume which is used to allocate all static content to our reverse proxy.


  **./nginx/default.conf:/etc/nginx/conf.d/default.conf** to move our configuration for the nginx reverse proxy to the nginx container.
  

The setup of the reverse proxy is under the nginx folder below the InternshipsApp folder.

**default.conf**

```default.conf
upstream internship_app {
   server web:8000;
}

server {
    listen 80;
    location /static/ {
        include  /etc/nginx/mime.types;
        alias /var/www/static/html/;
    }

    location / {
        proxy_pass http://internship_app;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_redirect off;
    }

}

 ```

Under the static folder you will be able to see all the static folders that **nginx** is able to serve.

## Deploy
 
 
 1.cd internships_tracker && cp example.env .env

 2.open the .env file
 
  2.1 set your postgres db creds
     
     

     DB_DATABASE_NAME= 
     
     
     DB_USERNAME=
     
     
     DB_PASSWORD=
     
     
     DB_HOST=db
     
     
     DB_PORT=5432
     
     
  We always recommend 5432 for postgresql db  port, as it also in the docker-compose iternships_db service option.
  
  
  **Otherwise** you will have to change the port in the **docker-compose.yml**
  
  You can always change it here :
  
         ports: - "5432:5432" 
      
  under the  **internships_db** service
  
  

  2.2 set your django superuser creds:
   
   ```DJANGO_SUPERUSER_PASSWORD=```
   
   
   ```DJANGO_SUPERUSER_USERNAME=```
   
   
   ```DJANGO_SUPERUSER_EMAIL=```


  2.3 set ```DJANGO_ALLOWED_HOSTS=localhost``` to run locally


  3. ```docker-compose up --build -d``` to run the stack for the **first time**
 
 
  4.[**localhost**](https://localhost) will redirect you to the intial page of internships internshipsystem_web service

 5.You are ready to go with [**https://localhost/admin**](https://localhost/admin), and create all the users you need.

 6.You can make live changes to the code , and wwsgi server in internships_web container reloads everytime when there is no runtime error.


## Steps that might be needed

 1.docker exec -it  **CAUTION(internship_web CONTAINER_ID)**  /bin/bash


 2.Since you enter  the container then you should run **python3 manage.py create superuser**
  
 
 3.Sometimes you might have to run **python3 manage.py makemigrations && python3 manage.py migrate ** but all is managed by the reload command in the gunicorn sever.

## License
[MIT](https://choosealicense.com/licenses/mit/)










 
