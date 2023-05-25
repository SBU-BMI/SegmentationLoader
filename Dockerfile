FROM mongo:4.2-bionic
RUN mv /etc/apt/sources.list.d/mongodb-org.list /tmp/mongodb-org.list && \
    apt-get update && \
    apt-get install -y curl && \
    curl -o /etc/apt/keyrings/mongodb.gpg https://pgp.mongodb.com/server-4.2.pub && \
    mv /tmp/mongodb-org.list /etc/apt/sources.list.d/mongodb-org.list;
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y wget git vim build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
RUN cd /usr/src && wget https://www.python.org/ftp/python/3.9.9/Python-3.9.9.tgz && tar xzf Python-3.9.9.tgz && cd Python-3.9.9 && ./configure --enable-optimizations && make altinstall
COPY ./app/loadfiles.sh /usr/bin/loadfiles
RUN chmod 0755 /usr/bin/loadfiles
COPY ./app/*.py /app/
COPY ./app/requirements.txt /app/
RUN pip3.9 install --upgrade pip && pip3.9 install -r /app/requirements.txt
WORKDIR /app
