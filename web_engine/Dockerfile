############################################################
# Dockerfile to build Flask App
############################################################

# Set the base image from https://hub.docker.com/_/python/
FROM python:3.6

# File Author / Maintainer
MAINTAINER Hossein Medy (hossein.medy@gmail.com)

################## BEGIN INSTALLATION ######################

# Update the repository sources list once more
RUN apt-get update

# Install Apache and some other handy packages
RUN apt-get install -y \
    apache2 \
	apache2-dev \
    vim less\
  && apt-get clean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

# Install the WSGI interface into Python
RUN pip install mod_wsgi

# intall application requirements in a separate step so that it doesn't invalidate Docker's cache
RUN mkdir /var/www/web_engin/
COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

##################### INSTALLATION END #####################

#copy the entire application 
ADD . /var/www/web_engine

# Create the upload folder with the permission  
RUN mkdir /tmp/uploads
RUN chmod 777 /tmp/uploads

WORKDIR /var/www/

# expose container ports for HTTP on 5000.
EXPOSE 5000

CMD mod_wsgi-express start-server web_engine/wsgi.py \
  --user www-data --group www-data \
  --port=5000 \
  --reload-on-changes \
  --log-to-terminal \
  --startup-log \
  --locale C.UTF-8 \
  --server-root=/etc/mod_wsgi-express-80

#WORKDIR /var/www/web_engine
#CMD python route.py

#CMD /bin/bash
#CMD /etc/mod_wsgi-express-80/apachectl start
