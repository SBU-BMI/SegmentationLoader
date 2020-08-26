FROM mongo:latest
RUN apt-get upgrade && apt-get update && apt-get install -y wget git vim build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
RUN cd /usr/src && wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz && tar xzf Python-3.7.3.tgz && cd Python-3.7.3 && ./configure --enable-optimizations && make altinstall
COPY ./app/loadfiles.sh /usr/bin/loadfiles
RUN chmod 0755 /usr/bin/loadfiles
COPY ./app/*.py /app/
COPY ./app/requirements.txt /app/
RUN pip3.7 install --upgrade pip && pip3.7 install -r /app/requirements.txt
WORKDIR /app

RUN chown -R 1001:0 /app && \
	chgrp -R 0 /app && \
    chmod -R g+rwX /app

RUN chown -R 1001:0 /data && \
	chgrp -R 0 /data && \
    chmod -R g+rwX /data

USER 1001

