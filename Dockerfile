# Use the official Python image with Alpine for a smaller footprint
FROM python:3.9.5-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies for building Python packages
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add --no-cache mariadb-connector-c-dev jpeg-dev zlib-dev libjpeg-turbo-dev postgresql-dev

# Install pip and upgrade to the latest version
RUN pip install --upgrade pip

# Copy the requirements file and install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Copy the project source code to the work directory
COPY . /usr/src/app/

COPY pokemon_data.csv /tmp/pokemon_data.csv

# Set executable permission for the entrypoint.sh file
RUN chmod +x /usr/src/app/entrypoint.sh

# Set the entrypoint to ensure the container is started with entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
