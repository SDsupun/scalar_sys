import hashlib
import os
import mysql
import time

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from mysql import connector
from mysql.connector import OperationalError

from page.sys_popup import SystemPopup


class LoginWindow(Screen):
    passwd = ObjectProperty()
    login_button = ObjectProperty()
    idm = ObjectProperty()

    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if self.manager.back_key and self.manager.current == "login_page":
            self.manager.back_key = False
            return False

        if self.manager.current != "login_page":
            self.passwd.focus = False
        if ~self.passwd.focus and ~self.login_button.focus and self.manager.current == "login_page":
            Clock.schedule_once(self.focus_input_text, 0.1)
        if self.login_button.focus and keycode == 40 and self.manager.current == "login_page":
            self.check_passwd()
            return True

    def focus_input_text(self, _):
        self.passwd.focus = True

    def check_passwd(self):
        try:
            hash_input = hashlib.md5(self.passwd.text.encode())
#            hidm = hashlib.md5(f'{self.idm}WhiteOwl*78'.encode())
            passwd_sql = f'''SELECT user_name, password FROM scalar_system.sys_user 
                    WHERE password='{hash_input.hexdigest()}' '''

            try:
                cursor = self.manager.db_conn.cursor()
                cursor.execute(passwd_sql)
                login_user_tharadi = ""
                for pw in cursor.fetchall():
                    login_user_tharadi = pw[0]

            except OperationalError:
                login_user_tharadi = 'no_db'

            # check device info file stat
            # dev_info_file = "/proc/cpuinfo"
            # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(dev_info_file)
            # if atime != mtime or mtime != ctime or ctime != atime:
            #     if gid != 0 and uid != 0:
            #         SystemPopup(title="App Security Checkup Failure!", notice="Exiting...").open()
            #         return False

            # with open(dev_info_file, "r") as device:
            #     if int(device.readline()[:13]) != 1422919052795:
            #         SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
            #         return False

            # check_sum = 0
            # with open(dev_info_file, "r") as device:
            #     for info in device:
            #         if 'Hardware' in info:
            #             if not 'BCM2835\n':
            #                 SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
            #                 return False
            #             else:
            #                 check_sum += 1
            #         elif 'Revision' in info:
            #             if not 'c03130\n':
            #                 SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
            #                 return False
            #             else:
            #                 check_sum += 1
            #         elif 'Serial' in info:
            #             if not '10000000939ded92\n' in info:
            #                 SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
            #                 return False
            #             else:
            #                 check_sum += 1

            #     if check_sum != 3:
            #         SystemPopup(title="App Security Checkup Failure!", notice="Exiting...").open()
            #         return False
                    
#            if hidm.hexdigest() != '4250c458b3ec06e94327203de99b41e0':
#
#                SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
#                # exit(132)
#                return False

            if login_user_tharadi == "admin":
                if ~self.login_button.focus:
                    self.manager.current = "main_page"
                    self.passwd.text = ''
                    self.manager.transition.direction = "left"
                    self.manager.get_screen('main_page').ids.main_setting_button.disabled = False
                    # Window.unbind(on_key_down=self._on_keyboard_down)
                    return True
                else:
                    return True
            elif login_user_tharadi == "operator":
                if ~self.login_button.focus:
                    self.manager.current = "main_page"
                    self.passwd.text = ''
                    self.manager.transition.direction = "left"
                    self.manager.get_screen('main_page').ids.main_setting_button.disabled = True
                    # Window.unbind(on_key_down=self._on_keyboard_down)
                    return True
                else:
                    return True

            elif login_user_tharadi == 'no_db':
                self.passwd.text = ''
                self.login_button.focus = False
                SystemPopup(title="Warning!", notice="No DB Connection!").open()
                return False
            else:
                # if ~self.passwd.focus and ~self.login_button.focus:
                #     return False
                self.passwd.text = ''
                self.login_button.focus = False
                SystemPopup(title="Warning!", notice="incorrect password!").open()
                return False

        except mysql.connector.errors.InterfaceError:
            self.passwd.text = ''
            self.login_button.focus = False
            self.passwd.focus = True
            SystemPopup(title="Warning!", notice="Database Error!").open()

            return False
