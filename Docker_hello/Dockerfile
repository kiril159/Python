FROM nginx

COPY authorized_keys .ssh/authorized_key
RUN apt-get update
RUN apt-get install -y  mc htop tcpdump openssh-server

