FROM mongo:latest

RUN apt-get upgrade && apt-get update && apt-get install -y wget git vim build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN cd /usr/src && wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz && tar xzf Python-3.7.3.tgz && cd Python-3.7.3 && ./configure --enable-optimizations && make altinstall

COPY ./requirements.txt /app/requirements.txt

RUN pip3.7 install --upgrade pip && pip3.7 install -r /app/requirements.txt

WORKDIR /app

