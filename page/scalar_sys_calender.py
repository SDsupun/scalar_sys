import datetime

from KivyCalendar import CalendarWidget
from KivyCalendar.calendar_ui import ButtonsGrid, DayAbbrWeekendLabel, DayAbbrLabel, DayNumWeekendButton, DayNumButton
from kivy.app import App
from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivy.properties import ReferenceListProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from KivyCalendar import calendar_data as cal_data


class DateSelect(TextInput):
    """
    Date picker is a textinput, if it focused shows popup with calendar
    which allows you to define the popup dimensions using pHint_x, pHint_y,
    and the pHint lists, for example in kv:
    DatePicker:
        pHint: 0.7,0.4
    would result in a size_hint of 0.7,0.4 being used to create the popup
    """
    pHint_x = NumericProperty(0.0)
    pHint_y = NumericProperty(0.0)
    pHint = ReferenceListProperty(pHint_x, pHint_y)
    pTitle = StringProperty()

    def __init__(self, touch_switch=False, **kwargs):
        super(DateSelect, self).__init__(**kwargs)
        self.touch_switch = touch_switch
        self.init_ui()

    def init_ui(self):
        self.text = cal_data.today_date()
        # Calendar
        self.cal = MyCalendarWidget(as_popup=True,
                                    touch_switch=self.touch_switch)
        # Popup
        self.popup = Popup(content=self.cal, on_dismiss=self.update_value,
                           title=self.pTitle, title_align='center', title_size=20, title_color=[1,1,0,1])
        self.cal.parent_popup = self.popup

        self.bind(focus=self.show_popup)

    def show_popup(self, isnt, val):
        """
        Open popup if textinput focused,
        and regardless update the popup size_hint
        """
        self.popup.size_hint = self.pHint
        self.popup.title = self.pTitle
        if val:
            # Automatically dismiss the keyboard
            # that results from the textInput
            Window.release_all_keyboards()
            self.popup.open()

    def update_value(self, inst):
        """ Update textinput value on popup close """

        self.text = "%s-%s-%s" % tuple((self.cal.active_date[-1], self.cal.active_date[-2], self.cal.active_date[-3]))
        self.focus = False


class MyCalendarWidget(CalendarWidget):
    inst = EventDispatcher()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        # check for date popup
        if isinstance(App.get_running_app().root_window.children[0], Popup):
            if App.get_running_app().root_window.children[0].title == 'From Date' \
                    or App.get_running_app().root_window.children[0].title == 'To Date':

                self.inst = instance
                if keycode == 78:
                    self.go_prev(instance)
                elif keycode == 75:
                    self.go_next(instance)
                elif keycode == 81:
                    new_dates = datetime.datetime(self.active_date[2],
                                                  self.active_date[1],
                                                  self.active_date[0]) + datetime.timedelta(days=7)

                    if self.active_date[1] == new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.clear_widgets()
                        self.init_ui()
                    elif self.active_date[1] > new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_prev(instance)
                    else:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_next(instance)
                elif keycode == 82:
                    new_dates = datetime.datetime(self.active_date[2],
                                                  self.active_date[1],
                                                  self.active_date[0]) + datetime.timedelta(days=-7)

                    if self.active_date[1] == new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.clear_widgets()
                        self.init_ui()
                    elif self.active_date[1] > new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_prev(instance)
                    else:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_next(instance)
                elif keycode == 79:
                    new_dates = datetime.datetime(self.active_date[2],
                                                  self.active_date[1],
                                                  self.active_date[0]) + datetime.timedelta(days=1)

                    if self.active_date[1] == new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.clear_widgets()
                        self.init_ui()
                    elif self.active_date[1] > new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_prev(instance)
                    else:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_next(instance)
                elif keycode == 80:
                    new_dates = datetime.datetime(self.active_date[2],
                                                  self.active_date[1],
                                                  self.active_date[0]) + datetime.timedelta(days=-1)

                    if self.active_date[1] == new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.clear_widgets()
                        self.init_ui()
                    elif self.active_date[1] > new_dates.month:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_prev(instance)
                    else:
                        self.active_date = [new_dates.day, new_dates.month, new_dates.year]
                        self.go_next(instance)
                else:
                    self.parent_popup.dismiss()
                    self.focus = False

    def create_month_scr(self, month, toogle_today=False):
        """ Screen with calendar for one month """

        scr = Screen()
        m = self.month_names_eng[self.active_date[1] - 1]
        scr.name = "%s-%s" % (m, self.active_date[2])  # like march-2015

        # Grid for days
        grid_layout = ButtonsGrid()
        scr.add_widget(grid_layout)

        # Days abbrs
        for i in range(7):
            if i >= 5:  # weekends
                l = DayAbbrWeekendLabel(text=self.days_abrs[i])
            else:  # work days
                l = DayAbbrLabel(text=self.days_abrs[i])

            grid_layout.add_widget(l)

        # Buttons with days numbers
        for week in month:
            for day in week:
                if day[1] >= 5:  # weekends
                    tbtn = DayNumWeekendButton(text=str(day[0]))
                else:  # work days
                    tbtn = DayNumButton(text=str(day[0]))

                tbtn.bind(on_press=self.get_btn_value)

                if toogle_today:
                    # Down today button
                    if day[0] == self.active_date[0] and day[2] == 1:
                        tbtn.state = "down"
                # Disable buttons with days from other months
                if day[2] == 0:
                    tbtn.disabled = True

                grid_layout.add_widget(tbtn)

        self.sm.add_widget(scr)
