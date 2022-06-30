FROM  python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/
RUN python3 manage.py migrate

#CMD [ "python", "manage.py", "runserver", "0.0.0.0:7000" ]