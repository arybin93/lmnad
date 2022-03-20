FROM python:3.7-slim

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

ARG PROJECT=lmnad

# Install Package Libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    default-libmysqlclient-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    vim \
    git \
    netcat \
    gettext \
    && rm -rf /var/lib/apt/lists/*

# Install any needed packages specified in requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /tmp/requirements.txt

# set work directory
WORKDIR /$PROJECT

# copy project
COPY . .
RUN mv wait-for /bin/wait-for && chmod +x /bin/wait-for && sed -i 's/\r//' /bin/wait-for

EXPOSE 8001

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
