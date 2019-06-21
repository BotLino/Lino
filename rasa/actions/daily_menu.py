import requests
import time
import json
from rasa_core_sdk import Action
from concurrent.futures import TimeoutError

DOWNLOAD_PATH = '/rasa/downloads'


class ActionDailyMenu(Action):
    def name(self):
        return "action_daily_menu"

    def run(self, dispatcher, tracker, domain):
        messages = []

        day = time.strftime('%A', time.localtime())

        menu_file = open(f'{DOWNLOAD_PATH}/general.json')
        response = json.load(menu_file)

        messages.append('Eai! Então... Pro café da manhã, nós teremos: ')

        breakfast_block = ""

        for label in response['DESJEJUM']:
            cell = str(label + ': ' + response['DESJEJUM'][label] + '\n')
            breakfast_block += cell

        messages.append(breakfast_block)

        messages.append('Já, para o almoço, teremos: ')

        lunch_block = ""

        for label in response['ALMOÇO']:
            cell = str(label + ' ' + response['ALMOÇO'][label] + '\n')
            lunch_block += cell

        messages.append(lunch_block)

        messages.append('E para a janta...')

        dinner_block = ""

        for label in response['JANTAR']:
            cell = str(label + ' ' + response['JANTAR'][label] + '\n')
            dinner_block += cell

        messages.append(dinner_block)

        for message in messages:
            dispatcher.utter_message(message)

        return []


class ActionNextMeal(Action):
    def name(self):
        return "action_next_meal"

    def run(self, dispatcher, tracker, domain):
        pass
