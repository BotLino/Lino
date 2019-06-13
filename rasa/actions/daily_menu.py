import requests
import time
from rasa_core_sdk import Action
from concurrent.futures import TimeoutError
import logging


class ActionDailyMenu(Action):
    def name(self):
        return "action_daily_menu"

    def run(self, dispatcher, tracker, domain):
        messages = []

        day = time.strftime('%A', time.localtime())

        # Change the url if you have your own webcrawler server
        try:
            response = requests.get(
                'http://webcrawler-ru.botlino.com.br/cardapio/{}'
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
