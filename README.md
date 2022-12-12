# OAuth 2.0 Implementation

OAuth 2.0 Implementation Sample using Python 3, FastAPI and PostgreSQL as the database

## TODOs
1. Scopes Implementation/Role Based Access Control
2. Implement other grant types
3. See and improve # TODO 

## Requirements
* [Python 3.8.1](https://www.python.org/downloads/release/python-381)
* [Package Manager](https://pip.pypa.io/en/stable/)
* [Postgresql](https://www.postgresql.org/download/)

## Installation
* Create a virtual environment
```bash
python3 -m venv venv
```
* Enable the virtualenvironment
```bash
source venv/bin/activate
```
* Install libraries
```bash
pip install -r requirements.txt
```
* Create database
* Create a environment variable file (rename/copy sample.env file to .env and update the values)
```bash
cp sample.env .env
```

## Usage
* Running the application
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
* Running the test cases
```bash
# be sure to run
pytest -v
```
* Running using Docker
Note: Install docker first before executing these commands and also don't forget to create .env file
```bash
sudo docker build -t sample-oauth2-implementation-image .
# --network="host" to connect to the local database setup
sudo docker run -d --name sample-oauth2-implementation-container --network="host" sample-oauth2-implementation-image
```

* Setting up NGINX for proxy to docker app
Note: Install nginx first before executing these instructions
    * [FOR DEVELOPMENT ONLY] Create your local domain name - if no public domain name yet
        1. Open the hosts file
        ```bash
        sudo vi /etc/hosts
        ```
        2. write your desired hostname inside the file and the file should look like the below text
        ```text
        127.0.0.1       localhost
        127.0.1.1       desiredhostname.abc

        # The following lines are desirable for IPv6 capable hosts
        ::1     ip6-localhost ip6-loopback
        fe00::0 ip6-localnet
        ff00::0 ip6-mcastprefix
        ff02::1 ip6-allnodes
        ff02::2 ip6-allrouters
        ```

    * Configure NGINX
        1. Create a configuration file
        ```bash
        sudo vi /etc/nginx/sites-available/sample-oauth2-implementation
        ```
        2. Write the configuration
        ```text
        server {
            server_name desiredhostname.abc;

            location / {
                proxy_pass http://localhost:8000/;
            }
        }
        ```
        3. Link the file to sites enabled
        ```bash
        sudo ln -s /etc/nginx/sites-available/sample-oauth2-implementation /etc/nginx/sites-enabled/
        ```
        4. Check if the nginx configuration have no issues
        ```bash
        sudo nginx -t
        ```
        5. restart or reload the NGINX
        ```bash
        sudo service nginx reload
        ```
    
    * Copy the link below and paste it in the browser to see if your setup is running successfully
    ```text
    desiredhostname.abc/docs
    ```

## API Documentation
* [Docs](http://localhost:8000/docs) - Swagger Documentation
