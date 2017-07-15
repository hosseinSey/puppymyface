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

# intall application requirements in this separate step so that it doesn't invalidate Docker's cache
COPY requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

##################### INSTALLATION END #####################

# Create the upload folder with the permission  
RUN mkdir /tmp/uploads
RUN chmod 777 /tmp/uploads

# expose container ports for HTTP on 5000 and for HTTPS on 443.
# If you are using the --https-only option for Apache,
# use --https-port 443 and expose 443 for https. Otherwise, there
# will be a mix up in the forwarding. 
EXPOSE 5000 443

#copy the entire application 
ADD . /var/www/web_engine

WORKDIR /var/www

# make certificates accessible only by the root user
RUN chmod 600 web_engine/ssl-certs/*

# For header buffer size, see this post: https://stackoverflow.com/a/24844743/7014331
#  --header-buffer-size 65536 \
#  --log-level info \
#--body-min-rate BYTES
#                        The number of bytes required to be sent as part of the
#                        request body to trigger a dynamic increase in the
#                        timeout on receiving the request body. Each time this
#                        number of bytes is received the timeout will be
#                        increased by 1 second up to any maximum specified by
#                        the maximum body timeout. Defaults to 500 bytes.

CMD mod_wsgi-express start-server web_engine/wsgi.py \
  --user www-data --group www-data \
  --port=5000 \
  --reload-on-changes \
  --log-to-terminal \
  --startup-log \
  --locale C.UTF-8 \
  --rewrite-rules web_engine/rewrite.conf \
  --server-root=/etc/mod_wsgi-express-80
  
#  --https-port 443 \
#  --server-name www.puppymyface.com \
#  --server-alias puppymyface.com \
#  --https-only \
#  --ssl-certificate-key-file ./web_engine/ssl-certs/server.key \
#  --ssl-certificate-file ./web_engine/ssl-certs/server.crt \
#  --ssl-certificate-chain-file ./web_engine/ssl-certs/gd_bundle-g2-g1.crt

#WORKDIR /var/www/web_engine
#CMD python route.py

#CMD /bin/bash
#CMD /etc/mod_wsgi-express-80/apachectl start
