#!/bin/bash
echo "Creating docker subnetwork named $1"
docker network create $1