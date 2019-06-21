import requests
import os
import time
import logging
import json
from concurrent.futures import TimeoutError
from rasa_core_sdk import Action

ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN', '')
API_URL = 'https://api.telegram.org'
PARSE = 'Markdown'
DOWNLOAD_PATH = '/rasa/downloads'


class ActionDailyBreakfast(Action):
    def name(self):
        return "action_daily_breakfast"

    def run(self, dispatcher, tracker, domain):
        messages = []

        day = time.strftime('%A', time.localtime())

        tracker_state = tracker.current_state()
        logging.warning(tracker_state)
        sender_id = tracker_state['sender_id']

        menu_file = open(f'{DOWNLOAD_PATH}/desjejum.json')
        response = json.load(menu_file)

        lunch_menu = ""

        for label in response:
            dish = str(
                '*' + label + '*' + ' ' +
                response[label] + '\n')
            lunch_menu += dish

        messages.append(lunch_menu)

        welcome_message = 'Eai! Então... Pro café, nós teremos: '

        data = requests.post(
            f'{API_URL}/bot{ACCESS_TOKEN}/sendMessage',
            data={
                'chat_id': sender_id,
                'text': welcome_message
            }
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
                requests.post(
                    f'{API_URL}/bot{ACCESS_TOKEN}/sendMessage',
                    data={
                        'chat_id': sender_id,
                        'text': message,
                        'parse_mode': PARSE
                    }
                )
        elif(messenger == "Facebook"):
            for message in messages:
                dispatcher.utter_message(message)

        return []
