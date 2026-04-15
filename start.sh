#!/bin/bash

# Démarrer SSH
/usr/sbin/sshd -D &

# Garder le conteneur actif
sleep infinity
