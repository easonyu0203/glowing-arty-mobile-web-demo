#!/bin/bash

# Tag the Docker image
docker tag arty-mobile-web-fd asia.gcr.io/glowing-arty/fd

# Push the Docker image to Google Container Registry
docker push asia.gcr.io/glowing-arty/fd
