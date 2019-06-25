from rasa_core_sdk import Action
from rasa_core_sdk.events import UserUttered

# Action to send a notification to user
class ActionTriggerNotification(Action):
    def name(self):
        return "action_another_notification"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('TA BOM MANO')
        tracker.update(
            UserUttered('Me manda notificações',
                        intent={
                            'name': 'asks_about_register_notifications',
                            'confidence': 1.0}))
        return []

# Action to remove notifications from user
class ActionTriggerUnregisterNotification(Action):
    def name(self):
        return "action_trigger_unregister_notification"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message('BELEZA VEI')

        tracker.update(
            UserUttered(
                'sem notificações',
                intent={
                    'name': 'asks_about_unregister_notification',
                    'confidence': 1.0
                }
            )
        )

        return []
