FROM python:3.6

ADD ./requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN pip uninstall -y tensorflow && pip install tensorflow==1.12.0

RUN mkdir /2018.2-Lino

ADD . /2018.2-Lino

WORKDIR /2018.2-Lino/rasa

ENV TRAINING_EPOCHS=450 \
    CREDENTIALS="credentials.yml"

CMD make train && python train-telegram.py
