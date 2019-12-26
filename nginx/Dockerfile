from nginx

# remove default config
RUN rm /etc/nginx/conf.d/default.conf

RUN apt-get update && apt-get install vim -y && apt-get install iputils-ping -y

# replace with own
COPY nginx.conf /etc/nginx/conf.d/
