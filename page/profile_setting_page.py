import base64

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from mysql.connector import OperationalError


class ProfileSettingWindow(Screen):
    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(ProfileSettingWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_once(self.get_company_info, 5)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.manager.back_key and self.manager.current == "profile_setting_page":
            self.manager.back_key = False
            return False

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "profile_setting_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "profile_setting_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "profile_setting_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "profile_setting_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                pass
            elif button_index == 2:
                self.manager.transition.direction = "left"
                self.manager.current = "printer_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True
            elif button_index == 1:
                self.manager.transition.direction = "left"
                self.manager.current = "advance_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "profile_setting_page":
            if text == '1':
                pass

            elif text == '2':
                self.manager.transition.direction = "left"
                self.manager.current = "printer_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '3':
                self.manager.transition.direction = "left"
                self.manager.current = "advance_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '4':
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.back_key = True

            elif text == '0':
                self.manager.transition.direction = "left"
                self.manager.current = "login_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.back_key = True

            return True

        if self.manager.current != "profile_setting_page":
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False

        return

    def get_company_info(self, _):
        get_company_info = '''SELECT company_name, address, telephone, email, fax, printer_format, cx_field_1, 
         cx_field_2, cx_field_1_inuse, cx_field_2_inuse FROM scalar_system.sys_setting'''
        try:
            cursor = self.manager.db_conn.cursor()
            cursor.execute(get_company_info)
            company_info_base64 = cursor.fetchone()
        except OperationalError:
            company_info_base64 = ['', '', '', '', '', 'Format-1', '', '', False, False]
        self.ids.company_name_text.text = base64.b64decode(company_info_base64[0].encode('ascii')).decode('ascii')
        self.ids.address_text.text = base64.b64decode(company_info_base64[1].encode('ascii')).decode('ascii')
        self.ids.tele_text.text = base64.b64decode(company_info_base64[2].encode('ascii')).decode('ascii')
        self.ids.email_text.text = base64.b64decode(company_info_base64[3].encode('ascii')).decode('ascii')
        self.ids.fax_text.text = base64.b64decode(company_info_base64[4].encode('ascii')).decode('ascii')

        # global variable for first_page and second_page
        self.manager.printer_format = company_info_base64[5]
        self.manager.cx_field_1 = base64.b64decode(company_info_base64[6].encode('ascii')).decode('ascii')
        self.manager.cx_field_2 = base64.b64decode(company_info_base64[7].encode('ascii')).decode('ascii')
        self.manager.cx_field_1_inuse = company_info_base64[8]
        self.manager.cx_field_2_inuse = company_info_base64[9]

        self.manager.get_screen('first_page').ids.cx1_name_text.text = self.manager.cx_field_1
        self.manager.get_screen('first_page').ids.cx2_name_text.text = self.manager.cx_field_2
        self.manager.get_screen('first_page').ids.cx1_name_text.opacity = 1 if company_info_base64[8] else 0
        self.manager.get_screen('first_page').ids.cx2_name_text.opacity = 1 if company_info_base64[9] else 0
        self.manager.get_screen('first_page').ids.cx1_text.opacity = 1 if company_info_base64[8] else 0
        self.manager.get_screen('first_page').ids.cx2_text.opacity = 1 if company_info_base64[9] else 0

        self.manager.get_screen('second_page').ids.cx1_name_text.text = self.manager.cx_field_1
        self.manager.get_screen('second_page').ids.cx2_name_text.text = self.manager.cx_field_2
        self.manager.get_screen('second_page').ids.cx1_name_text.opacity = 1 if company_info_base64[8] else 0
        self.manager.get_screen('second_page').ids.cx2_name_text.opacity = 1 if company_info_base64[9] else 0
        self.manager.get_screen('second_page').ids.cx1_text.opacity = 1 if company_info_base64[8] else 0
        self.manager.get_screen('second_page').ids.cx2_text.opacity = 1 if company_info_base64[9] else 0
        return

    def update_company_info(self, column, value):
        value_base64 = base64.b64encode(value.encode('ascii')).decode('ascii')
        update_column_sql = f'''UPDATE scalar_system.sys_setting SET {column}='{value_base64}' WHERE id=1'''
        cursor = self.manager.db_conn.cursor()
        cursor.execute(update_column_sql)
        cursor.execute('commit')
        self.get_company_info(1)
        return
