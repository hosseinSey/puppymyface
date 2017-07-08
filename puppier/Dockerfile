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
    vim less\
  && apt-get clean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

# intall application requirements in this separate step so that it doesn't invalidate Docker's cache
COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

##################### INSTALLATION END #####################

#copy the entire application 
ADD . /var/www/puppier

WORKDIR /var/www/

CMD python puppier/puppier_worker.py
