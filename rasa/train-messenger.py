
import logging
import os
import train

from rasa_core.utils import configure_colored_logging, AvailableEndpoints
from rasa_core.run import load_agent
from rasa_core.interpreter import NaturalLanguageInterpreter
from rasa_core.channels.facebook import FacebookInput


logger = logging.getLogger(__name__)

VERIFY = os.getenv('VERIFY', '')
SECRET = os.getenv('SECRET', '')
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')


def run(core_dir, nlu_dir):
    _endpoints = AvailableEndpoints.read_endpoints('endpoints.yml')
    _interpreter = NaturalLanguageInterpreter.create(nlu_dir)

    input_channel = FacebookInput(
        fb_verify=VERIFY,
        # you need tell facebook this token, to confirm your URL
        fb_secret=SECRET,  # your app secret
        fb_access_token=FACEBOOK_ACCESS_TOKEN
        # token for the page you subscribed to
    )

    _agent = load_agent(core_dir,
                        interpreter=_interpreter,
                        endpoints=_endpoints)

    _agent.handle_channels(
        [input_channel], 5001, serve_forever=True
    )


if __name__ == '__main__':
    configure_colored_logging(loglevel='DEBUG')

    logger.info("Train NLU")
    logger.info("Train Dialogue")
    train.train_dialogue(
        'domain.yml',
        'models/dialogue',
        'data/stories/',
        'policy_config.yml'
    )
    logger.info("Run")
    run('models/dialogue', 'models/nlu/current')
