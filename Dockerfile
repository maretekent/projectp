FROM python:3.6
ARG ENVIRONMENT
ENV ENVIRONMENT=$ENVIRONMENT
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

#BEGIN TEMPORARY STATICS STOP GAP
RUN apt-get update
RUN apt-get -y install gnupg \
    apt-utils \
    apt-transport-https \
    curl \
    zip

RUN pip install --upgrade pip

# Install Python deps
RUN pip install --no-cache-dir -r ./requirements/${ENVIRONMENT}.txt

RUN python3 manage.py collectstatic --noinput

CMD ./devops/scripts/wait-for-it.sh -t 300 db:5432 && ./devops/scripts/run.sh
