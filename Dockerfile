FROM python:3.8.1
# setup a working directory
WORKDIR /code
# copy the requirements to be installed
COPY ./requirements.txt /code/requirements.txt
# install the requirements
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# copy important files to the working directory
COPY ./api /code/api
COPY ./models /code/models
COPY ./utilities /code/utilities
COPY ./app.py /code/app.py
COPY ./.env /code/.env
# expose the port where the application will be running
EXPOSE 8000
# run the command
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
# if using nginx use the cmd below
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]