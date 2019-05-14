import logging
import os
import train

from rasa_core.channels.telegram import TelegramInput
from rasa_core.utils import configure_colored_logging, AvailableEndpoints
from rasa_core.run import load_agent
from rasa_core.interpreter import NaturalLanguageInterpreter


logger = logging.getLogger(__name__)


def run(core_dir, nlu_dir):
    _endpoints = AvailableEndpoints.read_endpoints('endpoints.yml')
    _interpreter = NaturalLanguageInterpreter.create(nlu_dir)

    input_channel = TelegramInput(
        access_token=os.getenv('TELEGRAM_ACCESS_TOKEN', ''),
        verify=os.getenv('VERIFY', ''),
        webhook_url=os.getenv('WEBHOOK_URL', '')
    )

    _agent = load_agent(core_dir,
                        interpreter=_interpreter,
                        endpoints=_endpoints)

    _agent.handle_channels(
        [input_channel], 5002, serve_forever=True
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
