# Docker file for building the required system starting from Ubuntu 20.04 image
FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y curl apt-utils apt-transport-https debconf-utils \
    gcc build-essential libsasl2-dev python-dev libldap2-dev libssl-dev ldap-utils python3-pip \
    netcat net-tools  libpq-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /appinternships
ENV PATH=$PATH:/appinternships/.local/bin
COPY requirements.txt /reqs/
RUN pip install -r /reqs/requirements.txt
RUN pip install django-phonenumber-field[phonenumbers]
COPY ./internships_tracker /appinternships
RUN chmod +x /appinternships/hua_intern_init.sh
CMD /appinternships/hua_intern_init.sh