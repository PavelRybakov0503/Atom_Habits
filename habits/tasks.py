from datetime import datetime, timedelta

import pytz
from celery import shared_task

from config import settings
from habits.models import Habit
from habits.services import send_telegram_message


@shared_task
def telegram_notification():
    zone = pytz.timezone(settings.TIME_ZONE)
    current_time = datetime.now(zone)
    current_time_less = current_time - timedelta(minutes=5)
    habits = Habit.objects.filter(
        time__lte=current_time.time(), time__gte=current_time_less.time()
    )
    for habit in habits:
        user_tg = habit.user.tg_chat_id
        if user_tg:
            message = f"Я буду {habit.action} в {habit.time} в {habit.place}"
            send_telegram_message(message, user_tg)
