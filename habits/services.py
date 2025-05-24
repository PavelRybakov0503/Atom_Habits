import requests

from config.settings import TG_BOT_TOKEN


def send_telegram_message(message, chat_id):
    """Отправка сообщения через Telegram"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    response = requests.get(
        f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage",
        params=params,
        timeout=10,
    )
    if not response.ok:
        raise RuntimeError("Не удалось отправить сообщение Telegram")
