FROM python:3
ADD python/run.py /
ADD python/config.json /
ADD python/requirements.txt /
ADD python/cryptoalarm /cryptoalarm
RUN pip install -r requirements.txt
#RUN ./run.py --init
#CMD sleep 3600
CMD [ "python", "./run.py" ]
