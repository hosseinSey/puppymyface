############################################################
# Dockerfile to build Flask app with Nginx and Gunicorn
############################################################

# Set the base image from https://hub.docker.com/_/python/
FROM python:3.6

# File Author / Maintainer
MAINTAINER Hossein Medy (hossein.medy@gmail.com)

# install application requirements
COPY requirements.txt /web_engine/requirements.txt
RUN pip install -r /web_engine/requirements.txt

# Set the application working directory
WORKDIR /web_engine

# Copy the code from the current folder to /web_engine inside the container
ADD . /web_engine

# download and add external libraries and utilities
RUN git clone https://github.com/TeMedy/home_made_utils.git
RUN cp home_made_utils/file_utils.py /web_engine/src/

# Make port 5000 available for links and/or publish
EXPOSE 5000

# Define our command to be run when launching the container
CMD gunicorn route:app -c gunicorn_config.py
#CMD /bin/bash
