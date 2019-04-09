import os
from rasa_core.actions.action import Action
import requests

# If you want to use your own bot to development add the bot token as
# second parameters
TELEGRAM_ACCESS_TOKEN = os.getenv('TELEGRAM_ACCESS_TOKEN', '')


class ActionCalendar(Action):
    def name(self):
        return "action_calendar"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Calma aí, rapidinho!')
        dispatcher.utter_message('Vou buscar isso daí para você')
        crawlerRegister = 'https://webcrawler-matricula.botlino.com.br'
        requests.get(f'{crawlerRegister}/registration/downloadPdf')
        data = {
            'text': 'Aqui está o calendário de matrícula. '
                    'Nele você pode adquirir informações de datas sobre: '
                    'trancamento geral, parcial, período de matrícula, '
                    'pré-matrícula, ajuste...',
            'image': f'{crawlerRegister}/registration/downloadPdf'
        }
        dispatcher.utter_response(data)

        return []
