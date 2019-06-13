import requests
import os
import time
import logging
from concurrent.futures import TimeoutError
from rasa_core_sdk import Action

ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN', '')
API_URL = 'https://api.telegram.org'
PARSE = 'Markdown'


class ActionDailyLunch(Action):
    def name(self):
        return "action_daily_lunch"

    def run(self, dispatcher, tracker, domain):
        messages = []

        day = time.strftime('%A', time.localtime())

        tracker_state = tracker.current_state()
        logging.warning(tracker_state)
        sender_id = tracker_state['sender_id']

        try:
            response = requests.get(
                'http://webcrawler-ru.botlino.com.br/cardapio/{}/almoço'
                .format(day),
                timeout=3
            ).json()
        except TimeoutError as timeouterror:
            dispatcher.utter_message(
                "Tentei pegar o cardápio mas minha net não cooperou..."
                " Tenta pedir mais tarde, vou tentar resolver esse"
                " problema o mais rápido possível!"
            )
            return []
        except Exception as exception:
            dispatcher.utter_message(
                " Tive um probleminha em acessar o cardápio do RU. "
                "Tô tentando resolver o problema o mais rápido possível!"
            )
            return []

        lunch_menu = ""

        for label in response:
            dish = str(
                '*' + label + '*' + ' ' + response[label] + '\n'
                )
            lunch_menu += dish

        messages.append(lunch_menu)

        welcome_message = 'Eai! Então... Pro almoço, nós teremos: '

        data = requests.get(
            'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}'
            .format(ACCESS_TOKEN, sender_id, welcome_message)
        ).json()
        messenger = ""
        # Check user is from Telegram or Facebook
        if not data['ok']:
            dispatcher.utter_message(welcome_message)
            messenger = "Facebook"
        else:
            messenger = "Telegram"

        if(messenger == "Telegram"):
            for message in messages:
                requests.get(
                    '{}/bot{}/sendMessage?chat_id={}&text={}&parse_mode={}'
                    .format(
                        API_URL, ACCESS_TOKEN, sender_id, message, PARSE
                    )
                )
        elif(messenger == "Facebook"):
            for message in messages:
                dispatcher.utter_message(message)

        return []
