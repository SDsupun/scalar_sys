import base64

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen
from mysql.connector import OperationalError, ProgrammingError


class PrinterDropDown(DropDown):
    pass


class PrinterSettingWindow(Screen):
    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(PrinterSettingWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        Clock.schedule_once(self.get_printer_info, 5)
        Clock.schedule_once(self.create_dropdown, 5)
        self.printer_select_dropdown = PrinterDropDown()

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.manager.back_key and self.manager.current == "printer_setting_page":
            self.manager.back_key = False
            return False

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "printer_setting_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "printer_setting_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "printer_setting_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "printer_setting_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                self.manager.transition.direction = "left"
                self.manager.current = "profile_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True
            elif button_index == 2:
                pass
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
        if 'alt' in modifiers and self.manager.current == "printer_setting_page":
            if text == '1':
                self.manager.transition.direction = "left"
                self.manager.current = "profile_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '2':
                pass

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

        if self.manager.current != "printer_setting_page":
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False

        return

    def get_printer_info(self, _):
        get_printer_info = '''SELECT printer_format, cx_field_1, cx_field_2 FROM scalar_system.sys_setting'''
        # cursor = self.manager.db_conn.cursor()
        # cursor.execute("SELECT printer_format, cx_field_1, cx_field_2 FROM scalar_system.sys_setting")
        try:
            cursor = self.manager.db_conn.cursor()
            cursor.execute(get_printer_info)
            printer_info_base64 = cursor.fetchone()
        except OperationalError:
            printer_info_base64 = ['Format-1', '', '']
        self.ids.cx_field_1_name_text.text = base64.b64decode(printer_info_base64[1].encode('ascii')).decode('ascii')
        self.ids.cx_field_2_name_text.text = base64.b64decode(printer_info_base64[2].encode('ascii')).decode('ascii')
        self.ids.printer_select_button.text = printer_info_base64[0]

        get_printer_info = f'''SELECT footer_info FROM scalar_system.ticket_format 
        WHERE format="{printer_info_base64[0]}" '''

        try:
            cursor = self.manager.db_conn.cursor()
            cursor.execute(get_printer_info)
            printer_info_base64 = cursor.fetchone()
        except OperationalError:
            printer_info_base64 = ['']
        self.ids.company_footer_text.text = base64.b64decode(printer_info_base64[0].encode('ascii')).decode('ascii')

    def update_printer_info(self, column, value):
        value_base64 = base64.b64encode(value.encode('ascii')).decode('ascii')
        if column == 'cx_field_1' and len(value) > 1:
            update_column_sql = f'''UPDATE scalar_system.sys_setting SET {column}='{value_base64}', 
                        cx_field_1_inuse=True WHERE id=1'''
            self.manager.cx_field_1 = value
            self.manager.cx_field_1_inuse = True

            self.manager.get_screen('first_page').ids.cx1_name_text.text = self.manager.cx_field_1
            self.manager.get_screen('first_page').ids.cx1_name_text.opacity = 1
            self.manager.get_screen('first_page').ids.cx1_text.opacity = 1

            self.manager.get_screen('second_page').ids.cx1_name_text.text = self.manager.cx_field_1
            self.manager.get_screen('second_page').ids.cx1_name_text.opacity = 1
            self.manager.get_screen('second_page').ids.cx1_text.opacity = 1

        elif column == 'cx_field_2' and len(value) > 1:
            update_column_sql = f'''UPDATE scalar_system.sys_setting SET {column}='{value_base64}', 
                        cx_field_2_inuse=True WHERE id=1'''
            self.manager.cx_field_2 = value
            self.manager.cx_field_2_inuse = True

            self.manager.get_screen('first_page').ids.cx2_name_text.text = self.manager.cx_field_2
            self.manager.get_screen('first_page').ids.cx2_name_text.opacity = 1
            self.manager.get_screen('first_page').ids.cx2_text.opacity = 1

            self.manager.get_screen('second_page').ids.cx2_name_text.text = self.manager.cx_field_2
            self.manager.get_screen('second_page').ids.cx2_name_text.opacity = 1
            self.manager.get_screen('second_page').ids.cx2_text.opacity = 1

        elif column == 'cx_field_1' and len(value) <= 1:
            update_column_sql = f'''UPDATE scalar_system.sys_setting SET {column}='{value_base64}', 
                        cx_field_1_inuse=False WHERE id=1'''
            self.manager.cx_field_1 = value
            self.manager.cx_field_1_inuse = False

            self.manager.get_screen('first_page').ids.cx1_name_text.text = self.manager.cx_field_1
            self.manager.get_screen('first_page').ids.cx1_name_text.opacity = 0
            self.manager.get_screen('first_page').ids.cx1_text.opacity = 0

            self.manager.get_screen('second_page').ids.cx1_name_text.text = self.manager.cx_field_1
            self.manager.get_screen('second_page').ids.cx1_name_text.opacity = 0
            self.manager.get_screen('second_page').ids.cx1_text.opacity = 0

        elif column == 'cx_field_2' and len(value) <= 1:
            update_column_sql = f'''UPDATE scalar_system.sys_setting SET {column}='{value_base64}', 
                        cx_field_2_inuse=False WHERE id=1'''
            self.manager.cx_field_2 = value
            self.manager.cx_field_2_inuse = False

            self.manager.get_screen('first_page').ids.cx2_name_text.text = self.manager.cx_field_2
            self.manager.get_screen('first_page').ids.cx2_name_text.opacity = 0
            self.manager.get_screen('first_page').ids.cx2_text.opacity = 0

            self.manager.get_screen('second_page').ids.cx2_name_text.text = self.manager.cx_field_2
            self.manager.get_screen('second_page').ids.cx2_name_text.opacity = 0
            self.manager.get_screen('second_page').ids.cx2_text.opacity = 0

        elif column == 'footer_info':
            update_column_sql = f'''UPDATE scalar_system.ticket_format SET {column}='{value_base64}' 
            WHERE format="{self.ids.printer_select_button.text}" '''

        else:
            return False

        cursor = self.manager.db_conn.cursor()
        cursor.execute(update_column_sql)
        cursor.execute('commit')

        return True

    def set_printer_format(self, printer_format):
        update_printer_sql = f'''UPDATE scalar_system.sys_setting SET 
            printer_format='{printer_format}' WHERE id=1'''

        cursor = self.manager.db_conn.cursor()
        cursor.execute(update_printer_sql)
        cursor.execute('commit')

        self.ids.printer_select_button.text = printer_format
        self.manager.printer_format = printer_format

        get_printer_footer_info = f'''SELECT footer_info FROM scalar_system.ticket_format
                WHERE format="{printer_format}" '''

        try:
            cursor = self.manager.db_conn.cursor()
            cursor.execute(get_printer_footer_info)
            printer_info_base64 = cursor.fetchone()
        except OperationalError:
            printer_info_base64 = ['']
        self.ids.company_footer_text.text = base64.b64decode(printer_info_base64[0].encode('ascii')).decode('ascii')

        return True

    def create_dropdown(self, _):
        self.ids.printer_select_button.bind(on_release=self.printer_select_dropdown.open)
        self.printer_select_dropdown.bind(on_select=lambda instance, x: self.set_printer_format(x))
