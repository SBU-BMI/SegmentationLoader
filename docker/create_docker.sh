#!/usr/bin/env bash

cp ../*.py ./app
cd compose && docker-compose up -d
