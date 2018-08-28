FROM python:3
ADD run.py /
ADD config.json /
ADD requirements.txt /
ADD cryptoalarm /cryptoalarm
RUN pip install -r requirements.txt
#CMD sleep 3600
CMD [ "python", "./run.py" ]
