# Play.Excel
Please follow the below steps after cloning this repository:
  - Make sure that you have the following programs installed in your system
    - pip
    - virtualenv
    - mysql
  - Create a virtualenv (one that would contain this repository)
    ```sh
    $ virtualenv --python=python3 <your_env_name>
    ```
  - Install the requirements as follow
    ```sh
    $ pip install -r requirements.txt
    ```
  - Setup the MySQL db as follows
    - Open MySQL shell
      ```sh
      $ mysql -u <user> -p
      ```
    - Inside shell
      ```
      >> create database <your_db_name> character set utf8;
      >> create user <your_db_username> identified by '<your_db_pass>'
      >> grant all on <your_db_name>.* to <your_db_username>;
      >> flush privileges;
      >> exit
      ```
    - Provide <your_db_name>,<your_db_username> and <your_db_pass> in /playExcel/database_config.cnf file.
   
   - Test if everything is fine by running the development server
   ```sh
    $ python manage.py makemigrations
    $ python manage.py migrate
    $ python manage.py createsuperuser   
    $ python manage.py runserver
   ```
   - Setting up redis server
   ```sh
     $ sudo apt-get install redis-server
     $ sudo service redis-server start
   ```
Runnning the server:
  - Make sure you migrate everything before running the server.
  - Use "localhost" in place of 127.0.0.1. Eg: http://localhost:8000/ instead of http://127.0.0.1:8000/
  
Pushing to repository:
  - While adding file to git:
    - Please don't use ```git add . ```
    - Use ```git status``` to list all the modified/deleted files. Add/remove only those files which needs to be pushed, using the command ``` git add file_name [,filename]```
    - Don't add migration files to git.
  - If you have used any additional packages. Please add it to requirements.txt
  - Don't push database_config.cnf file after you have filled in your database credentials.
  - Give suitable commit message.
    
Other guidelines:
  - Go through the common.views file.
  - Please add suitable comments wherever needed. 
  - You can add details to readme.

Hashinclude specific:

  - Install docker. `sudo apt-get install docker.io` 
  - Start docker.service using `sudo systemctl start docker.service`
  - Build the docker image from Dockerfile `sudo docker build -t judge .` { Same directory as Dockerfile }
   
