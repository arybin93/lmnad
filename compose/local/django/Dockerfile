# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.5

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim

RUN apt-get install -y git

ARG PROJECT=lmnad
ARG PROJECT_DIR=/var/www/${PROJECT}

RUN mkdir -p $PROJECT_DIR

# Install any needed packages specified in requirements.txt
COPY requirements.txt $PROJECT_DIR/
RUN pip install -r $PROJECT_DIR/requirements.txt

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY . $PROJECT_DIR
WORKDIR $PROJECT_DIR
