#!/bin/sh

# Commands
# 1. makedata
# 2. train


cd /app
env $(cat .env | tr -d '\r') python3 manage.py $1