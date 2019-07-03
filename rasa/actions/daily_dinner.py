import requests
import time
import logging
from concurrent.futures import TimeoutError
from rasa_core_sdk import Action
from .constants import ACCESS_TOKEN, API_URL, PARSE


# Action to send dinner menu to user
class ActionDailyDinner(Action):
    def name(self):
        return "action_daily_dinner"

    def run(self, dispatcher, tracker, domain):
        day = self.get_current_day()

        try:
            menu = self.request_menu(day)
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

        menu_messages = self.format_menu(menu)

        welcome_message = 'Eai! Então... Pro jantar, nós teremos: '

        sender_id = self.get_sender_id(tracker)

        data = self.request_user_data(sender_id, welcome_message)

        if not data['ok']:
            dispatcher.utter_message(welcome_message)
            self.send_messages_to_facebook(dispatcher, menu_messages)
        else:
            self.send_messages_to_telegram(sender_id, menu_messages)

        return []

    def get_current_day(self):
        return time.strftime('%A', time.localtime())

    def get_sender_id(self, tracker):
        tracker_state = tracker.current_state()
        logging.warning(tracker_state)
        return tracker_state['sender_id']

    def request_menu(self, day):
        return requests.get(
            'http://webcrawler-ru.botlino.com.br/cardapio/{}/jantar'
            .format(day),
            timeout=3
        ).json()

    def format_menu(self, menu):
        formatted_menu = ""
        messages = []

        for label in menu:
            dish = str(
                '*' + label + '*' + ' ' + menu[label] + '\n'
                )
            formatted_menu += dish

        messages.append(formatted_menu)
        return messages

    def request_user_data(self, sender_id, message):
        data = requests.post(
            '{}/bot{}/sendMessage'
            .format(API_URL, ACCESS_TOKEN),
            data={
                'chat_id': sender_id,
                'text': message
            }
        ).json()

        return data

    def send_messages_to_telegram(self, sender_id, messages):
        for message in messages:
            requests.post(
                '{}/bot{}/sendMessage'
                .format(API_URL, ACCESS_TOKEN),
                data={
                    'chat_id': sender_id,
                    'text': message,
                    'parse_mode': PARSE
                }
            )

    def send_messages_to_facebook(self, dispatcher, messages):
        for message in messages:
            dispatcher.utter_message(message)
