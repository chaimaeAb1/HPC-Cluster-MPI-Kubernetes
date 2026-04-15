FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Configurer les DNS
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && \
    echo "nameserver 8.8.4.4" >> /etc/resolv.conf

# Installer tous les outils nécessaires + SSH
RUN apt-get update && apt-get install -y \
    build-essential \
    libopenmpi-dev \
    openmpi-bin \
    python3 \
    python3-pip \
    openssh-server \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Installer mpi4py
RUN pip3 install mpi4py

# Configurer SSH
RUN mkdir /var/run/sshd
RUN echo 'root:mpipassword' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Générer les clés SSH
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -N ''
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
RUN chmod 600 /root/.ssh/authorized_keys
RUN echo "StrictHostKeyChecking no" >> /root/.ssh/config

# Créer le répertoire de travail
WORKDIR /app

# Copier le programme Python
COPY mpi_sunshine_2022.py /app/mpi_sunshine_2022.py

# Script de démarrage
RUN echo '#!/bin/bash\n\
/usr/sbin/sshd\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
CMD ["sleep", "infinity"]
