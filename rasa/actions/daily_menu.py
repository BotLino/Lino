import requests
import time
from rasa_core_sdk import Action
from concurrent.futures import TimeoutError


class ActionDailyMenu(Action):
    def name(self):
        return "action_daily_menu"

    def run(self, dispatcher, tracker, domain):
        messages = []

        day = self.get_current_day()

        try:
            full_menu = self.request_menu(day)
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
        meal_name = 'DESJEJUM'
        breakfast_menu = self.format_menu(full_menu, meal_name)
        messages.append(breakfast_menu)

        messages.append('Já, para o almoço, teremos: ')
        meal_name = 'ALMOÇO'
        lunch_menu = self.format_menu(full_menu, meal_name)
        messages.append(lunch_menu)

        messages.append('E para a janta...')
        meal_name = 'JANTAR'
        dinner_menu = self.format_menu(full_menu, meal_name)
        messages.append(dinner_menu)

        self.send_messages(dispatcher, messages)

        return []

    def get_current_day(self):
        return time.strftime('%A', time.localtime())

    def request_menu(self, day):
        # Change the url if you have your own webcrawler server
        return requests.get(
            'http://webcrawler-ru.botlino.com.br/cardapio/{}'
            .format(day),
            timeout=3
        ).json()

    def format_menu(self, full_menu, meal_name):
        menu = ""

        for label in full_menu[meal_name]:
            dish = str(label + ' ' + full_menu[meal_name][label] + '\n')
            menu += dish

        return menu

    def send_messages(self, dispatcher, messages):
        for message in messages:
            dispatcher.utter_message(message)
