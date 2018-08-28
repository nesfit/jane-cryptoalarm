#!/bin/bash
echo "Downloading from GIT repo"
git submodule update --recursive --remote
echo "Removing old sources"
rm -rf ./cryptoalarm-web/laravel/
rm -rf ./cryptoalarm-app/python/
echo "Copy new sources"
cp -R ./sources/webapp/ ./cryptoalarm-web/laravel/
cp -R ./sources/cryptoalarm/ ./cryptoalarm-app/python

