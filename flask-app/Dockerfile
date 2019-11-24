FROM python:3.6.1-alpine
WORKDIR /app
ADD . /app
RUN pip install -r requirements.txt
RUN ["pip3", "install", "pipenv"]
RUN ["pipenv", "install"]
CMD pipenv run python app.py
