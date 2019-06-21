FROM python:3.6-slim

RUN apt update && apt install -y gcc make curl

ADD ./docker/actions.requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/actions.requirements.txt

ADD ./rasa/actions/ /rasa/actions/
ADD ./rasa/Makefile /rasa/Makefile
ADD ./cronjob/scripts/build_specific_menu.py /rasa/scripts/build_specific_menu.py

RUN mkdir /rasa/downloads/

WORKDIR rasa/

RUN python scripts/build_specific_menu.py

EXPOSE 5055

HEALTHCHECK --interval=300s --timeout=60s --retries=5 \
  CMD curl -f http://0.0.0.0:5055/health || exit 1

CMD make run-actions
