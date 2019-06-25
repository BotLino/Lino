import os

URI_TELEGRAM = os.getenv('URI_TELEGRAM', '')


def get_telegram_users(notification_type):
    client = MongoClient(URI_TELEGRAM)
    db = client['lino_telegram']

    users = db.users.find(
        {
            "notification": {
                "description": notification_type,
                "value": True
            }
        },
        {
            '_id': 0,
            'sender_id': 1
        }
    )

    return users
