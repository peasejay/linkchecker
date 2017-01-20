# simple dockerfile

FROM python:2.7

MAINTAINER Jeff Pease



# Install basic system dependencies
RUN apt-get update
RUN apt-get -y upgrade

# Install apt stuff
RUN apt-get -y install sqlite3 python-dev libmysqlclient-dev


# Host application directory in docker image
ADD . /code

ENV PYTHONPATH $PYTHONPATH:/usr/lib/pymodules/python2.7:/usr/lib/python2.7/dist-packages

# Install python modules
RUN pip install --upgrade pip
RUN pip install -r /code/requirements.txt



WORKDIR /code


CMD ./check_links.py



