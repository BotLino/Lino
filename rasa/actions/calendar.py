import os
from rasa_core_sdk import Action
import requests
from .constants import TELEGRAM_ACCESS_TOKEN

# Action to show registration schedule to user
class ActionCalendar(Action):
    def name(self):
        return "action_calendar"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('Calma aí, rapidinho!')
        dispatcher.utter_message('Vou buscar isso daí para você')
        crawlerRegister = 'https://webcrawler-matricula.botlino.com.br'
        try:
            requests.get(f'{crawlerRegister}/registration/downloadPdf',
                         timeout=3)
            data = {
                'text': 'Aqui está o calendário de matrícula. '
                        'Nele você pode adquirir informações de datas sobre: '
                        'trancamento geral, parcial, período de matrícula, '
                        'pré-matrícula, ajuste...',
                'image': f'{crawlerRegister}/registration/downloadPdf'
            }
            dispatcher.utter_template("utter_image",
                                      tracker,
                                      False,
                                      text=data.get('text'),
                                      image=data.get('image'))
        except Exception as exception:
            dispatcher.utter_message(
                "Tive um problema ao pegar o calendário acadêmico pra você... "
                "Tenta mais tarde! Para que houve um problema no site onde "
                "busco..."
            )

        return []
