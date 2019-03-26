import datetime
from rasa_core.actions.action import Action


class ActionSendWeekMenu(Action):
    def name(self):
        return "action_send_week_menu"

    def run(self, dispatcher, tracker, domain):
        crawler_url = 'https://webcrawler-ru.lappis.rocks'
        img_path = '/cardapio/pdf'
        timestamp = datetime.datetime.now().strftime("%d-%m-%Y")
        img_timestamp = f'?time={timestamp}'

        try:
            response = requests.get(
                f'{crawler_url}{img_path}{img_timestamp}',
                timeout=3
            )

            data = {
                'text': 'Tá aqui o cardápio da semana. '
                        'Aprecie com moderação :)',
                'image': f'{crawler_url}{img_path}{img_timestamp}'
            }
            dispatcher.utter_response(data)
        except Exception as exceptions:
            dispatcher.utter_message(
                "Não consegui pegar o cardápio da semana... "
                "Acho que aconteceu um problema com o site do RU. "
                "Tenta depois! O problema vai resolver em algum momento kk"
            )

        return []
