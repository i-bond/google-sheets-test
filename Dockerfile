FROM python:3.8.3
RUN apt-get update -qq && apt-get install vim nano jq jo -qqq

RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/



