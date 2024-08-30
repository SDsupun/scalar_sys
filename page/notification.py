from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout


class Notification(FloatLayout):
    notification = ObjectProperty()
    popup_ok_button = ObjectProperty()

    def __init__(self, notice, **kwargs):
        super().__init__(**kwargs)
        self.notification.text = notice

    def set_notification(self, notification):
        self.notification.text = notification
        return
