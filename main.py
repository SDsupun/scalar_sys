import kivy
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.app import App
from kivy.core.window import Window

Config.set('kivy', 'exit_on_escape', '0')
kivy.require('1.0.7')

from sysCom.scalar_com import ReadScalar
from page.login_page import LoginWindow
from page.main_page import MainWindow
from page.first_page import FirstWindow
from page.selectableGrid import SelectableGrid
from page.second_page import SecondWindow
from page.multi_page import MultiWindow
# from page.scalar_sys_calender import DateSelect
from page.report_page import ReportWindow
from page.print_page import PrintWindow
from page.profile_setting_page import ProfileSettingWindow
from page.printer_setting_page import PrinterSettingWindow
from page.advance_setting_page import AdvanceSettingWindow
from page.page_manager import PageManager


class PWHApp(App):

    def build(self):
        self.icon = 'pageStyle/icon_2/logo-2.png'
        return Builder.load_file("main.kv")


if __name__ == '__main__':
    PWHApp().run()
