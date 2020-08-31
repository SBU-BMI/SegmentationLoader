FROM mongo:3.6
RUN apt-get upgrade && apt-get update && apt-get install -y wget git vim build-essential checkinstall
RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN useradd -u 1001 -r -g 0 -d /app -s /sbin/nologin -c "Default Application User" default \
&& mkdir -p /app \
&& chown -R 1001:0 /app && chmod -R g+rwX /app

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

RUN mkdir -p /mongodb/db && \
	chown -R 1001:0 /mongodb && \
	chgrp -R 0 /mongodb && \
    chmod -R g+rwX /mongodb

USER 1001

CMD /usr/bin/mongod --dbpath /mongodb/db

