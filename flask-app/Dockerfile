FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk add --no-cache curl
COPY . .

# uWSGI is the server that runs on the WSGI specs. 
CMD ["uwsgi", "app.ini"]

# Alpine has no bash, but 'sh', so get into container using:
# docker exec -it <name> sh
