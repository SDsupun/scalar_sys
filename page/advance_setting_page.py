import hashlib

from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from mysql.connector import OperationalError
from page.sys_popup import SystemPopup


class AdvanceSettingWindow(Screen):
    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(AdvanceSettingWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.manager.back_key and self.manager.current == "advance_setting_page":
            self.manager.back_key = False
            return False

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "advance_setting_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "advance_setting_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "advance_setting_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "advance_setting_page":
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
                self.manager.transition.direction = "left"
                self.manager.current = "printer_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True
            elif button_index == 1:
                pass
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "advance_setting_page":
            if text == '1':
                self.manager.transition.direction = "left"
                self.manager.current = "profile_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '2':
                self.manager.transition.direction = "left"
                self.manager.current = "printer_setting_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '3':
                pass

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

        if self.manager.current != "advance_setting_page":
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False

        return

    def update_admin_passwd(self):
        if self.ids.set_admin_passwd_1.text == self.ids.set_admin_passwd_2.text:
            hash_input = hashlib.md5(self.ids.set_admin_passwd_1.text.encode())
            update_admin_pw_sql = f'''UPDATE scalar_system.sys_user SET password='{hash_input.hexdigest()}' 
                WHERE user_name='admin' '''
            cursor = self.manager.db_conn.cursor()
            cursor.execute(update_admin_pw_sql)
            cursor.execute('commit')
            self.ids.set_admin_passwd_1.text = ''
            self.ids.set_admin_passwd_2.text = ''
            return True
        else:
            SystemPopup(title="Info", notice="Password Doesn't Match!").open()

    def update_operator_passwd(self):
        if self.ids.set_operator_passwd_1.text == self.ids.set_operator_passwd_2.text:
            hash_input = hashlib.md5(self.ids.set_operator_passwd_1.text.encode())
            update_operator_pw_sql = f'''UPDATE scalar_system.sys_user SET password='{hash_input.hexdigest()}' 
                WHERE user_name='operator' '''
            cursor = self.manager.db_conn.cursor()
            cursor.execute(update_operator_pw_sql)
            cursor.execute('commit')
            self.ids.set_operator_passwd_1.text = ''
            self.ids.set_operator_passwd_2.text = ''
            return True
        else:
            SystemPopup(title="Info", notice="Password Doesn't Match!").open()
    
    def scalar_db_flush(self):
    
        hash_input = hashlib.md5(self.ids.db_flush_auth_passwd.text.encode())
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
            self.ids.db_flush_auth_passwd.text = ""
            SystemPopup(title="Warning", notice="Task Failed!\n No DB").open()
            
        if login_user_tharadi == "admin":
        	
            ticket1_flush_sql = '''DELETE FROM first_ticket'''
            ticket2_flush_sql = '''DELETE FROM second_ticket'''
            lookup_flush_sql = '''DELETE FROM first_lookup'''
            
            try:
                cursor = self.manager.db_conn.cursor()
                cursor.execute(ticket1_flush_sql)
                cursor.execute('commit')
                cursor.execute(ticket2_flush_sql)
                cursor.execute('commit')
                cursor.execute(lookup_flush_sql)
                cursor.execute('commit')
                SystemPopup(title="Info", notice="DB cleared").open()
                self.ids.db_flush_auth_passwd.text = ""

            except OperationalError:
                self.ids.db_flush_auth_passwd.text = ""
                SystemPopup(title="Warning", notice="Task Failed!\n No DB").open()
		        
        else:
            self.ids.db_flush_auth_passwd.text = ""
            SystemPopup(title="Info", notice="Task Failed!\n Wrong Password").open()



