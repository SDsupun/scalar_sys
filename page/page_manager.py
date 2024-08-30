import os

from datetime import datetime

from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager
from mysql import connector

from page.sys_popup import SystemPopup
from sysCom.scalar_com import ReadScalar


class PageManager(ScreenManager):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.readScalar = ReadScalar()
        Clock.schedule_interval(self.update_weight, 1)
        Clock.schedule_interval(self.update_time, 2)
        self.back_key = False

        # global variables
        self.printer_format = 'Format-1'
        self.cx_field_1 = ''
        self.cx_field_2 = ''
        self.cx_field_1_inuse = False
        self.cx_field_2_inuse = False
        self.first_weight_count = 0
        self.second_weight_count = 0

        try:
            self.db_conn = connector.connect(host="localhost", user="scal_user", password="tH@r@236",
                                             database="scalar_system")

        except:
            self.db_conn = connector.connect()

    # update weight fields
    def update_weight(self, dt):
        weight = self.readScalar.get_weight()
        try:
            weight = int(weight)
            if self.current == 'first_page':
                self.get_screen('first_page').ids.first_weight_text.text = f'{weight} kg'
            else:
                self.get_screen('first_page').ids.first_weight_text.text = '-reading-'

            if self.current == 'second_page':
                self.get_screen('second_page').ids.second_weight_text.text = f'{weight} kg'
            else:
                self.get_screen('second_page').ids.second_weight_text.text = '-reading-'

        except ValueError:
            self.readScalar.set_scalar()
            weight = '--'
            self.get_screen('first_page').ids.first_weight_text.text = 'no device'
            self.get_screen('second_page').ids.second_weight_text.text = 'no device'

        self.get_screen('main_page').ids.weight_top_text.text = f'{weight} kg'

        self.get_screen('first_page').ids.weight_top_text.text = f'{weight} kg'

        self.get_screen('second_page').ids.weight_top_text.text = f'{weight} kg'

        return

    def update_time(self, dt):

        time_str = datetime.strftime(datetime.now(), '%Y/%m/%d %H:%M:%S')
        self.get_screen('main_page').ids.date_time_top_text.text = time_str
        self.get_screen('first_page').ids.date_time_top_text.text = time_str
        self.get_screen('second_page').ids.date_time_top_text.text = time_str

        self.get_screen('first_page').ids.datetime_text.text = time_str
        self.get_screen('second_page').ids.datetime_2_text.text = time_str

        self.get_screen('main_page').ids.first_count_top_text.text = f'First Weights: {self.first_weight_count}'
        self.get_screen('main_page').ids.second_count_top_text.text = f'Second Weights: {self.second_weight_count}'
        self.get_screen('first_page').ids.first_count_top_text.text = f'First Weights: {self.first_weight_count}'
        self.get_screen('first_page').ids.second_count_top_text.text = f'Second Weights: {self.second_weight_count}'
        self.get_screen('second_page').ids.first_count_top_text.text = f'First Weights: {self.first_weight_count}'
        self.get_screen('second_page').ids.second_count_top_text.text = f'Second Weights: {self.second_weight_count}'

        return

    # set start focus
    def page_focus(self):
        self.back_key = True
        if self.current == 'login_page':
            self.get_screen('login_page').ids.passwd.focus = True
            self.get_screen('first_page').clear_ticket()
            self.get_screen('second_page').clear_ticket()
            self.get_screen('report_page').clear_record()
            self.get_screen('print_page').clear_search()

        elif self.current == 'main_page':
            self.get_screen('main_page').ids.main_sel_grid.focus = True
        elif self.current == 'first_page':
            self.get_screen('first_page').ids.vehicle_text.focus = True
        elif self.current == 'second_page':
            self.get_screen('second_page').ids.vehicle_text.focus = True
        elif self.current == 'multi_page':
            self.get_screen('multi_page').ids.vehicle_text.focus = True
        elif self.current == 'report_page':
            self.get_screen('report_page').ids.ticket_text.focus = True
        elif self.current == 'print_page':
            self.get_screen('print_page').ids.ticket_text.focus = True
        elif self.current == 'print_page':
            self.get_screen('profile_setting_page').ids.company_name_text.focus = True

        # check device info file stat
        # dev_info_file = "/proc/cpuinfo"
        # (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(dev_info_file)
        # if atime != mtime or mtime != ctime or ctime != atime:
        #     SystemPopup(title="App Security Checkup Failure!", notice="Exiting...").open()
        #     return False
        # if gid != 0 and uid != 0:
        #     SystemPopup(title="App Security Checkup Failure!", notice="Exiting...").open()
        #     return False

        # check_sum = 0
        # with open(dev_info_file, "r") as device:
        #     for info in device:
        #         if 'Hardware' in info:
        #             if not 'BCM2835\n':
        #                 SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
        #                 return False
        #             else:
        #                 check_sum += 1
        #         if 'Revision' in info:
        #             if not 'c03130\n':
        #                 SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
        #                 return False
        #             else:
        #                 check_sum += 1
        #         if 'Serial' in info:
        #             if not '10000000939ded92\n' in info:
        #                 SystemPopup(title="Unknown Hardware!", notice="Exiting...").open()
        #                 return False
        #             else:
        #                 check_sum += 1

        #     if check_sum != 3:
        #         SystemPopup(title="App Security Checkup Failure!", notice="Exiting...").open()
        #         return False

        # return

    def warning_popup(self):
        pass
