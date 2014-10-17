FROM phusion/baseimage:0.9.15
MAINTAINER Leonard Camacho <leonard.camacho@gmail.com>

# Set correct environment variables.
ENV HOME /root

# Disable ssh server because we don't need it for local devlopment.
RUN rm -rf /etc/service/sshd /etc/my_init.d/00_regen_ssh_host_keys.sh

# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

# Install Ubuntu dependencies.
RUN apt-get update && apt-get install -y python python-dev python-pip postgresql libpq-dev memcached libxml2-dev libxslt1-dev

# Copy script to run services at boot like memcached, etc.
RUN mkdir -p /etc/my_init.d
ADD services.sh /etc/my_init.d/services.sh

ADD . /airmozilla

WORKDIR /airmozilla

# Install python dependencies.
RUN pip install -r requirements/compiled.txt

# Comment next line if your not going to run tests
RUN pip install -r requirements/dev.txt

USER postgres

# Create airmozilla database and run migrations
RUN /etc/init.d/postgresql start && psql -c "ALTER ROLE postgres WITH ENCRYPTED PASSWORD 'mozilla'" &&\
    createdb -T template0 -E UTF8 airmozilla && ./manage.py syncdb --noinput && ./manage.py migrate

USER root

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

EXPOSE 8000