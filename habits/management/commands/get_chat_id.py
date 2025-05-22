import requests

from django.core.management import BaseCommand

from habits.models import Habit
from config.settings import TELEGRAM_API_TOKEN, TELEGRAM_URL_BOT


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        chai_id = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/getUpdates')
        print(f"\nИнформация о ТГ боте:\n{chai_id.json()}")
        print(f"\nВаш чат id: {chai_id.json()['result'][0]['message']['from']['id']}\n")

        habits = Habit.objects.all()
        for habit in habits:
            message = f'Внимание!' \
                      f'\n{habit}'
            params = {
                'chat_id': habit.owner.telegram_chat_id,
                'text': message
            }
            create_url_message_to_user = (f'{TELEGRAM_URL_BOT}{TELEGRAM_API_TOKEN}/sendMessage?chat_id='
                                          f'{habit.owner.telegram_chat_id}&text={message}')

            print(create_url_message_to_user)
            requests.get(f'{TELEGRAM_URL_BOT}{TELEGRAM_API_TOKEN}/sendMessage?', params=params)
