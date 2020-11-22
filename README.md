# LMNAD project

[![Build Status](https://travis-ci.com/arybin93/lmnad.svg?branch=master)](https://travis-ci.com/arybin93/lmnad)

Web Application of Laboratory of Modeling of Natural and Anthropogenic Disasters ([LMNAD](https://lmnad.nntu.ru))
from Nizhny Novgorod

---

## Getting Started
These instructions for getting the copy of project in local machine for testing and development goals

### Installation prerequisites

- git 

### Preferred platform
- linux 

### Setting up project
1. Clone project from github:
    ```
    git clone git@github.com:arybin93/lmnad.git
    ```
2. Install python 3.5.4
    Download Python 3.5.4 from [python.org](https://www.python.org) according to your OS.

3. Create virtual environment
    ```
    python3.5 -m venv <directory_for_venv>
    ```

4. Install dependencies
    ```
    pip install -r requirements.txt
    ```
    For installing [mysqlclient](https://pypi.org/project/mysqlclient/)

5. Install MySQL Server 5.5.53
    Example of [instructions](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-20-04) 
    Create database `lmnad_db`, set your user and password in `lmnad/project/settings/dev.py`

6. Run migrate
    ```
   # activate virtual environment
   # from project directory
   python manage.py migrate
   ```
   This command create tables in your databases

7. Run server
    ```
   python manage.py runserver
    ```
   Check url from browser [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Project LMNAD without data was deployed locally, congratulations!


### Setting up Database
If you need data from site LMNAD locally (for testing and development goals),  
send request for getting data to arybin93@email.com

### Running celery worker
1. Install Rabbit MQ
2. Run celery with active venv and from root of project lmnad:
   ```
   celery -A project worker -l info  -P solo
   ```

### Setting up project via Docker
    TBD

### Deployment
    TBD

### Backup
    TBD
