#!/bin/bash

sudo apt update
sudo apt upgrade

ssh-keygen -t ed25519 -C "cchilder@mail.usf.edu"
cat .ssh/id_ed25519.pub

git clone git@github.com:codyc4321/stocks_backend.git
# git clone https://github.com/codyc4321/stocks_backend.git

cd stocks_backend

sudo apt install gunicorn
sudo apt install python3-pip

pip install -r requirements.txt

# SET UP .env FILE WITH SECRET KEY

# to start the server:
gunicorn --bind 0.0.0.0:8000 dividends_project.wsgi
