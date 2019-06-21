import requests
import json
import time
import os

RUCRAWLER_URL = os.getenv('RUCRAWLER_URL', 'http://webcrawler-ru.botlino.com.br/cardapio/')
DOWNLOAD_PATH = "/rasa/downloads/"

class BuildSpecificMenu():
    def run_specifics(self):
        day = time.strftime('%A', time.localtime())
        response = self.get_general_menu(day)

        for key in response.keys():
            self.write_in_file(key.lower(), response[key])

    def run_general(self, menu_name):
        day = time.strftime('%A', time.localtime())
        response = self.get_general_menu(day)
        self.write_in_file(menu_name, response)

    def get_general_menu(self, day):
        try:
            response = requests.get(
                f'{RUCRAWLER_URL}{day}',
                timeout=3
            ).json()

            return response

        except TimeoutError as timeouterror:
            return {
                'response': False,
                'error': 'Timeout Exception retring exceed.'
            }

        except Exception as exception:
            return {
                'response': False,
                'error': 'General Exception retring exceed.'
            }

    def write_in_file(self, menu_name, response):
        file = open(f'{DOWNLOAD_PATH}{menu_name}.json', 'w')
        data = json.dumps(response, indent=4, ensure_ascii=False)
        file.write(data)
        file.close()

if __name__ == '__main__':
    builder = BuildSpecificMenu()
    builder.run_general('general')
    builder.run_specifics()
