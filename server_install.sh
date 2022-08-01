#!/bin/bash

sudo apt update
sudo apt upgrade

ssh-keygen -t ed25519 -C "cchilder@mail.usf.edu"
cat .ssh/id_ed25519.pub

git clone git@github.com:codyc4321/stocks_backend.git
