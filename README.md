# Play.Excel
Please follow the below steps after cloning this repository:
  - Make sure that you have the following programs installed in your system
    - pip
    - virtualenv
    - mysql
  - Create a virtualenv (one that would contain this repository)
  - Install the requirements as follow
    ```sh
    $ pip install -r requirements.txt
    ```
  - Setup the MySQL db as follows
    - Open MySQL shell
      ```sh
      $ sudo mysql
      ```
    - Inside shell
      ```
      >> create database <your_db_name>;
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
    $ python createsuperuser   
    $ python manage.py runserver
   ```
