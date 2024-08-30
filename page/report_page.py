from kivy.app import App
from kivy.core.window import Window
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from page.sys_popup import SystemPopup
from sysCom.reportDoc import ReportFormat1


class ReportWindow(Screen):
    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(ReportWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.edit_text_field = 0
        self.first_time_load = True
        self.record = []
        self.clear_event = False 

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        # stop executing previous page command
        if self.manager.back_key and self.manager.current == "report_page":
            self.manager.back_key = False
            return False

        if self.manager.current == "report_page" and self.first_time_load:
            self.first_time_load = False
            self.text_field_count = 5

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "report_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "report_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "report_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        # arrow key direction on side bar
        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "report_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                self.search()
            elif button_index == 2:
                self.print_record()
            elif button_index == 1:
                self.clear_record()
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "report_page":
            if text == '1':
                self.search()

            elif text == '2':
                self.print_record()

            elif text == '3':
                self.clear_record()

            elif text == '4':
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '0':
                self.manager.transition.direction = "left"
                self.manager.current = "login_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        if self.text_in_grid.focus and self.manager.current == "report_page":
            if keycode == 81:
                if self.edit_text_field < self.text_field_count:
                    if ~isinstance(App.get_running_app().root_window.children[0], Popup):
                        self.edit_text_field += 1

            elif keycode == 82:
                if self.edit_text_field > 0:
                    if ~isinstance(App.get_running_app().root_window.children[0], Popup):
                        self.edit_text_field -= 1

            else:
                return False

            if self.edit_text_field == 0 and self.ids.ticket_text.opacity == 1:
                self.ids.ticket_text.focus = True
            elif self.edit_text_field == 1 and self.ids.vehicle_text.opacity == 1:
                self.ids.vehicle_text.focus = True
            elif self.edit_text_field == 2 and self.ids.customer_text.opacity == 1:
                self.ids.customer_text.focus = True
            elif self.edit_text_field == 3 and self.ids.plant_text.opacity == 1:
                self.ids.plant_text.focus = True
            elif self.edit_text_field == 4 and self.ids.driver_text.opacity == 1:
                self.ids.driver_text.focus = True
            elif self.edit_text_field == 5 and self.ids.operator_text.opacity == 1:
                self.clear_event = False
                self.ids.operator_text.focus = True
            elif self.edit_text_field == 6 and self.ids.from_date_text.opacity == 1:
                self.ids.from_date_text.focus = True
            elif self.edit_text_field == 7 and self.ids.to_date_text.opacity == 1:
                self.ids.to_date_text.focus = True
   
            # change scroll view
            if not self.ids.ticket_text.opacity:
                if keycode == 81:
                    self.ids.search_result_text.scroll_y += 1/( len(self.ids.search_result_text.children[0].children) / 12)

                elif keycode == 82:
                    self.ids.search_result_text.scroll_y -= 1/( len(self.ids.search_result_text.children[0].children) / 12)

                else:
                    return False
        
            return True

        if self.manager.current != "report_page":
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False
         

        return

    def search(self):
        get_search_sql = f'''SELECT * FROM scalar_system.second_ticket WHERE
                                CAST(ticket_no as CHAR) LIKE '{self.ids.ticket_text.text}%'
                                AND vehicle_no LIKE '{self.ids.vehicle_text.text}%'
                                AND customer LIKE '{self.ids.customer_text.text}%'
                                AND plant_no LIKE '{self.ids.plant_text.text}%'
                                AND customer LIKE '{self.ids.customer_text.text}%'
                                AND driver_name LIKE '{self.ids.driver_text.text}%'
                                AND operator_name LIKE '{self.ids.operator_text.text}%'
                                AND first_datetime >= CAST('{self.ids.from_date_text.text}' AS DATETIME)
                                AND first_datetime <= CAST('{self.ids.to_date_text.text} 23:59:59' AS DATETIME) 
                                ORDER BY ticket_no DESC '''

        cursor = self.manager.db_conn.cursor()
        cursor.execute(get_search_sql)

        search_layout = GridLayout(cols=10, padding=10, size_hint_x=None, size_hint_y=None, row_default_height=50)
        search_layout.add_widget(Label(text='Ticket No', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Time-1', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Time-2', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Vehicle No', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Customer', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Product', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        #search_layout.add_widget(Label(text='Plant No', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        #search_layout.add_widget(Label(text='Driver', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Operator', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        #search_layout.add_widget(Label(text='CX-1', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        #search_layout.add_widget(Label(text='CX-2', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='First Weight', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Second Weight', color=(0, 0, 0, 1), size_hint_x=None, width=150))
        search_layout.add_widget(Label(text='Net Weight', color=(0, 0, 0, 1), size_hint_x=None, width=150))

        self.record = [['Ticket No', 'Time-1', 'Time-2', 'Vehicle No', 'Customer', 'Product', 'Plant No',
                        'Driver', 'Operator', 'CX-1', 'CX-2', 'First Weight', 'Second Weight', 'Net Weight']]
        
        self.ids.ticket_text.opacity = 0
        self.ids.vehicle_text.opacity = 0
        self.ids.customer_text.opacity = 0
        self.ids.plant_text.opacity = 0
        self.ids.driver_text.opacity = 0
        self.ids.operator_text.opacity = 0
        self.ids.from_date_text.opacity = 0
        self.ids.to_date_text.opacity = 0
        
        self.ids.ticket_label.opacity = 0
        self.ids.vehicle_label.opacity = 0
        self.ids.customer_label.opacity = 0
        self.ids.plant_label.opacity = 0
        self.ids.driver_label.opacity = 0
        self.ids.operator_label.opacity = 0
        self.ids.from_date_label.opacity = 0
        self.ids.to_date_label.opacity = 0
        
        #self.ids.text_in_grid.clear_widgets()
        self.ids.text_in_grid.size_hint_x = 0.01
        
        for row in cursor.fetchall():
            record_row = []
            for ri, r in enumerate(row):
                record_row.append(str(r))
                if ri not in (6, 7, 9, 10):
                    search_layout.add_widget(Label(text=str(r), color=(0, 0, 0, 1), size_hint_x=None, width=150))
            self.record.append(record_row)
        try:
            self.ids.search_result_text.remove_widget(self.ids.search_result_text.children[0])
        except IndexError:
            pass
        self.ids.search_result_text.add_widget(search_layout)
        DampedScrollEffect.spring_constant = 0.5
        DampedScrollEffect.edge_damping = 0.5
        self.ids.search_result_text.effect_cls = DampedScrollEffect
        return

    def print_record(self):
        record_doc = ReportFormat1()
        set_data_ok = record_doc.set_search_info('', self.record, column_count=14)

        if set_data_ok:
            print_ok = record_doc.print_record()

            if print_ok:
                SystemPopup(title="Info", notice="Report is Printing!").open()
            else:
                SystemPopup(title="Warning!", notice="Report Printing Failed!").open()
        else:
            pass

        self.record = [[]]
        return

    def clear_record(self):
        
        self.clear_event = True 
        self.ids.text_in_grid.size_hint_x = 1
        self.ids.ticket_text.opacity = 1
        self.ids.vehicle_text.opacity = 1
        self.ids.customer_text.opacity = 1
        self.ids.plant_text.opacity = 1
        self.ids.driver_text.opacity = 1
        self.ids.operator_text.opacity = 1
        self.ids.from_date_text.opacity = 1
        self.ids.to_date_text.opacity = 1
        
        self.ids.ticket_label.opacity = 1
        self.ids.vehicle_label.opacity = 1
        self.ids.customer_label.opacity = 1
        self.ids.plant_label.opacity = 1
        self.ids.driver_label.opacity = 1
        self.ids.operator_label.opacity = 1
        self.ids.from_date_label.opacity = 1
        self.ids.to_date_label.opacity = 1
        
        self.ids.vehicle_text.text = ''
        self.ids.ticket_text.text = ''
        self.ids.customer_text.text = ''
        self.ids.plant_text.text = ''
        self.ids.driver_text.text = ''
        self.ids.operator_text.text = ''
        self.ids.from_date_text.text = ''
        self.ids.to_date_text.text = ''
        
        
        try:
            self.ids.search_result_text.remove_widget(self.ids.search_result_text.children[0])
        except IndexError:
            pass


            
