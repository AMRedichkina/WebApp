# A website with recipes for creating a list of products
![example workflow](https://github.com/NIK-TIGER-BILL/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)  
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)



Foodgram is implemented for publishing recipes. Authorized users can subscribe to their favorite authors,
add recipes to favorites, to purchases, download a shopping list of ingredients for recipes added to purchases

## The project has been launched and is available [at](http://51.250.73.138/recipes)


## Preparing and launching a project from the repository

### Step 1. Clone the repository:
```
git clone git@github.com:AMRedichkina/Website-with-recipes-for-creating-a-list-of-products.git
```
## To work with a remote server (on ubuntu):
* Log in to your remote server

* Install docker on the server:
```
sudo apt install docker.io 
```
* Install docker-compose on the server:
```
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
* Edit the infra/nginx.conf file locally and enter your IP in the server_name line
* Copy the docker-compose files.yml and nginx.conf from the infra directory to the server:
```
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

* Create .env file and enter:
    ```
    DB_ENGINE=<django.db.backends.postgresql>
    DB_NAME=<database name postgres>
    DB_USER=<user database>
    DB_PASSWORD=<password>
    DB_HOST=<db>
    DB_PORT=<5432>
    SECRET_KEY=<secret key of project django>
    ```
* To work with Workflow, add environment variables to Secrets GitHub for work
(the same as in .env. except the secret key and also the next secrets):
    
    DOCKER_PASSWORD=<пароль от DockerHub>
    DOCKER_USERNAME=<имя пользователя>
 

    USER=<username для подключения к серверу>
    HOST=<IP сервера>
    PASSPHRASE=<пароль для сервера, если он установлен>
    SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

    TELEGRAM_TO=<ID чата, в который придет сообщение>
    TELEGRAM_TOKEN=<токен вашего бота>
    ```
    Workflow consists of three steps:
    - Checking the code for compliance with PEP8
    - Build and publish a backend image on DockerHub. 
    - Automatic deployment to a remote server.
    - Sending notifications in telegram chat.
  
* On the server, build docker-compose:
```
sudo docker-compose up -d --build
```
* After a successful build on the server, run the commands (only after the first deployment):
    - Collect static files:
    ```
    sudo docker-compose exec backend python manage.py collectstatic --noinput
    ```
    - Apply migrations:
    ```
    sudo docker-compose exec backend python manage.py migrate --noinput
    ```
    - Upload ingredients to the database (optional):
    *If you do not specify the file, by default it will be selected ingredients.json*
    ```
    sudo docker-compose exec backend python manage.py load_ingredients <Название файла из директории data>
    ```
    - Create a Django Superuser:
    ```
    sudo docker-compose exec backend python manage.py createsuperuser
    ```
    - The project will be available by your IP
