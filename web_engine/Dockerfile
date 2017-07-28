############################################################
# Dockerfile to build Flask app with Nginx and Gunicorn
############################################################

# Set the base image from https://hub.docker.com/_/python/
FROM python:3.6

# File Author / Maintainer
MAINTAINER Hossein Medy (hossein.medy@gmail.com)

################## INSTALL PACKAGES / PIP ######################

# Update the repository sources list once more
RUN apt-get update

RUN apt-get install -y \
    vim less \
  && apt-get clean \
  && apt-get autoremove \
  && rm -rf /var/lib/apt/lists/*

# install application requirements in a separate step
COPY requirements.txt /web_engine/requirements.txt
RUN pip install -r /web_engine/requirements.txt

################## COPYING FILES, etc. ###################
ADD . /web_engine
WORKDIR /web_engine
EXPOSE 5000

# download and add libraries and utilities   
RUN git clone https://github.com/TeMedy/home_made_utils.git 
RUN cp home_made_utils/file_utils.py /web_engine/src/

################## ENTRY TO CONTAINER ###################
CMD gunicorn route:app -c gunicorn_config.py
#CMD /bin/bash
