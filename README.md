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

## API Documentation
* [Docs](http://localhost:8000/docs) - Swagger Documentation
