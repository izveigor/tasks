#!/usr/bin/bash

docker-compose -f backend/account/docker-compose.yml up -d --build
docker-compose -f backend/tasks/docker-compose.yml up -d --build
docker-compose -f backend/notifications/docker-compose.yml up -d --build
docker-compose -f backend/gateway/docker-compose.yml up -d --build
docker-compose -f frontend/docker-compose.yml up -d --build

exec "$@"