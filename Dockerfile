FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y \
    git \
    cowsay \
    fortune \
    netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/nyrahul/wisecow.git . && \
    chmod +x wisecow.sh

ENV PATH="/usr/games:${PATH}"

RUN useradd -m wisecow && \
    chown -R wisecow:wisecow /app

USER wisecow

EXPOSE 4499

CMD ["./wisecow.sh"]