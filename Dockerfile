FROM amd64/debian:latest

RUN apt-get update -yqq && apt-get install -yqq \
    curl \
    unzip \
    zip \
    bzip2 \
    gzip \
    gettext \
    python3 \
    python3-pip

RUN pip3 install \
    Jinja2

ADD ./scripts /scripts
ADD ./config /config

RUN chmod -R +x /scripts

EXPOSE 27275/udp
EXPOSE 27276/udp
EXPOSE 27277/udp

VOLUME [ "/data" ]

CMD [ "/scripts/start.sh" ]