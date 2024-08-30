from kivy.clock import Clock
from kivy.uix.popup import Popup
from sys import exit

from page.notification import Notification


class SystemPopup(Popup):

    def __init__(self, notice, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.dismiss, 2)
        self.content = Notification(notice=notice)
        self.bind(on_dismiss=self.call_me)
        self.size_hint = (None, None)
        self.size = (300, 150)
        self.auto_dismiss = True
        self.title_size = 18

    def call_me(self, inst):
        if self.title == "Unknown Hardware!":
            exit(12)
        elif self.title == "App Security Checkup Failure!":
            exit(13)
