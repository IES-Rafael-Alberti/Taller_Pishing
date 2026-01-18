# Usamos Debian como base
FROM debian:latest

# Instalamos lo necesario para Zphisher
RUN apt-get update && apt-get install -y \
    git \
    curl \
    php \
    unzip \
    wget \
    sudo \
    net-tools \
    && rm -rf /var/lib/apt/lists/*

# Descargamos Zphisher
WORKDIR /opt
RUN git clone https://github.com/htr-tech/zphisher.git

# Arrancamos Zphisher

RUN chmod +x zphisher.sh
ENTRYPOINT ["./zphisher.sh"]