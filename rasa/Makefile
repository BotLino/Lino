train-nlu:
	python -m rasa_nlu.train -c nlu_config.yml --fixed_model_name current --data data/intents/ -o models --project nlu --verbose

train-core:
	python train.py

train: train-nlu train-core

run-telegram:
	python -m rasa_core.run -d models/dialogue -u models/nlu/current --port 5002 --credentials credentials.yml --endpoints endpoints.yml

run-facebook:
	python train.py run-facebook

run-actions:
	python -m rasa_core_sdk.endpoint --actions actions
