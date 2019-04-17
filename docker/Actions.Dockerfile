FROM python:3.6-slim

RUN apt update && apt install -y gcc make curl

ADD ./docker/actions.requirements.txt /tmp/

RUN pip install --upgrade pip && \
    pip install -r /tmp/actions.requirements.txt

ADD ./rasa/actions/ /rasa/actions/
ADD ./rasa/Makefile /rasa/Makefile

WORKDIR rasa/

EXPOSE 5055

HEALTHCHECK --interval=300s --timeout=60s --retries=5 \
  CMD curl -f http://0.0.0.0:5055/health || exit 1

CMD make run-actions
