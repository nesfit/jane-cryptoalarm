FROM python:3
ADD python/requirements.txt /
RUN pip install -r requirements.txt

ADD python/run.py /
ADD python/config.json /
ADD python/cryptoalarm /cryptoalarm

#RUN sleep 3600
CMD [ "python", "./run.py" ]
