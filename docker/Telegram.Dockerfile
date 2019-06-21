FROM python:3.6

RUN apt-get update && \
    apt-get install -y cron

ADD ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN pip uninstall -y tensorflow && pip install tensorflow==1.12.0

RUN mkdir /Lino

ADD . /Lino

WORKDIR /Lino/rasa

ENV TRAINING_EPOCHS=450 \
    CREDENTIALS="credentials.yml"

# Setting cron
COPY cronjob/lino-crontab /etc/cron.d/lino-crontab

RUN chmod 0644 /etc/cron.d/lino-crontab

RUN touch /var/log/cron.log

RUN /usr/bin/crontab /etc/cron.d/lino-crontab

CMD make train && python train-telegram.py
