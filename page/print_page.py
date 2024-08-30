from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from page.sys_popup import SystemPopup


class RecordDropDown(DropDown):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max_height = 44 * 6


class PrintWindow(Screen):
    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(PrintWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.edit_text_field = 0
        self.first_time_load = True
        self.record_select_dropdown = RecordDropDown()
        self.search_result = [['Please search']]
        Clock.schedule_once(self.create_dropdown, 5)
        self.selected_ticket = []
        self.current_showing_ticket = 0
        self.clear_event = False

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        # stop executing previous page command
        if self.manager.back_key and self.manager.current == "print_page":
            self.manager.back_key = False
            return False

        if self.manager.current == "print_page" and self.first_time_load:
            self.first_time_load = False
            self.text_field_count = 4
            self.current_showing_ticket = 0

        # change current showing ticket from keyboard
        if self.manager.current == "print_page" and keycode == 78:
            try:
                current_ticket = f'{self.search_result[self.current_showing_ticket][0]},'
            except IndexError:
                return False
            self.show_selected(current_ticket)
            self.current_showing_ticket += 1
            if len(self.search_result) <= self.current_showing_ticket:
                self.current_showing_ticket -= 1
            return True

        elif self.manager.current == "print_page" and keycode == 75:
            try:
                current_ticket = f'{self.search_result[self.current_showing_ticket][0]},'
            except IndexError:
                return False
            self.show_selected(current_ticket)
            self.current_showing_ticket -= 1
            if len(self.search_result) <= abs(self.current_showing_ticket):
                self.current_showing_ticket += 1
            return True

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "print_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "print_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "print_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        # arrow key direction on side bar
        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "print_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                self.search()
            elif button_index == 2:
                self.print_ticket()
            elif button_index == 1:
                self.clear_search()
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "print_page":
            if text == '1':
                self.search()

            elif text == '2':
                self.print_ticket()

            elif text == '3':
                self.clear_search()

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

        if self.text_in_grid.focus and self.manager.current == "print_page":
            if keycode == 81:
                if self.edit_text_field < self.text_field_count:
                    self.edit_text_field += 1

            elif keycode == 82:
                if self.edit_text_field > 0:
                    self.edit_text_field -= 1

            else:
                return False

            if self.edit_text_field == 0:
                self.ids.ticket_text.focus = True
            elif self.edit_text_field == 1:
                self.ids.vehicle_text.focus = True
            elif self.edit_text_field == 2:
                self.ids.customer_text.focus = True
            elif self.edit_text_field == 3:
                self.ids.plant_text.focus = True
            elif self.edit_text_field == 4:
                self.ids.driver_text.focus = True
                self.clear_event = False
            elif self.edit_text_field == 5:
                self.ids.from_date_text.focus = True
            elif self.edit_text_field == 6:
                self.ids.to_date_text.focus = True

            return True

        if self.manager.current != "print_page":
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
                                AND first_datetime >= CAST('{self.ids.from_date_text.text}' AS DATETIME)
                                AND first_datetime <= CAST('{self.ids.to_date_text.text} 23:59:59' AS DATETIME) 
                                ORDER BY ticket_no DESC'''

        cursor = self.manager.db_conn.cursor()
        cursor.execute(get_search_sql)

        self.search_result = []
        self.record_select_dropdown.clear_widgets()

        for tk in cursor.fetchall():
            tmp = []
            for i in tk:
                tmp.append(str(i))

            self.search_result.append(tmp)
            search_tag = ', '.join((tmp[0], tmp[1], tmp[3]))
            btn = Button(text=search_tag, size_hint_y=None, height=44)
            self.record_select_dropdown.add_widget(btn)
            btn.bind(on_release=lambda btn: self.record_select_dropdown.select(btn.text))

    def create_dropdown(self, _):
        self.ids.record_select_button.bind(on_release=self.record_select_dropdown.open)
        self.record_select_dropdown.bind(on_select=lambda instance, x: self.show_selected(x))

    def show_selected(self, selected):
        title = ['Ticket No', 'Time-1', 'Time-2', 'Vehicle No', 'Customer', 'Product', 'Plant No',
                 'Driver', 'Operator', 'CX-1', 'CX-2', 'First Weight', 'Second Weight', 'Net Weight']
        self.ids.record_select_button.text = selected
        self.ids.show_result_layout.clear_widgets()
        self.selected_ticket = []
        for tk in self.search_result:
            if tk[0] == selected.split(',')[0]:
                for j, i in enumerate(tk):
                    label = Label(text=title[j], color=(0, 0, 0, 1))
                    label.font_size = label.height * 0.3

                    self.ids.show_result_layout.add_widget(label)
                    label = Label(text=i, color=(0, 0, 0, 1))
                    label.font_size = label.height * 0.3
                    self.ids.show_result_layout.add_widget(label)
                    self.selected_ticket.append(i)

    def print_ticket(self):

        if len(self.selected_ticket) == 0:
            SystemPopup(title="Warning!", notice="No Data to Print!").open()
            return False

        if self.manager.cx_field_1_inuse or self.manager.cx_field_2_inuse or self.manager.printer_format == 'Format-3':
            from sysCom.ticketDoc import TicketFormat3
            ticket = TicketFormat3()
            if self.manager.cx_field_1_inuse and self.manager.cx_field_2_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.selected_ticket[0]],
                     ['Time-1', self.selected_ticket[1]],
                     ['Time-2', self.selected_ticket[2]],
                     ['Vehicle No', self.selected_ticket[3]],
                     ['Customer', self.selected_ticket[4]],
                     ['Product', self.selected_ticket[5]],
                     ['Plant No', self.selected_ticket[6]],
                     ['Driver', self.selected_ticket[7]],
                     ['Operator', self.selected_ticket[8]],
                     [self.manager.cx_field_1, self.selected_ticket[9]],
                     [self.manager.cx_field_2, self.selected_ticket[10]],
                     ['First Weight', f'{self.selected_ticket[11]} kg'],
                     ['Second Weight', f'{self.selected_ticket[12]} kg'],
                     ['Net Weight', f'{self.selected_ticket[13]}']]
                )
            elif self.manager.cx_field_1_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.selected_ticket[0]],
                     ['Time-1', self.selected_ticket[1]],
                     ['Time-2', self.selected_ticket[2]],
                     ['Vehicle No', self.selected_ticket[3]],
                     ['Customer', self.selected_ticket[4]],
                     ['Product', self.selected_ticket[5]],
                     ['Plant No', self.selected_ticket[6]],
                     ['Driver', self.selected_ticket[7]],
                     ['Operator', self.selected_ticket[8]],
                     [self.manager.cx_field_1, self.selected_ticket[9]],
                     ['First Weight', f'{self.selected_ticket[11]} kg'],
                     ['Second Weight', f'{self.selected_ticket[12]} kg'],
                     ['Net Weight', f'{self.selected_ticket[13]}']]
                )
            elif self.manager.cx_field_2_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.selected_ticket[0]],
                     ['Time-1', self.selected_ticket[1]],
                     ['Time-2', self.selected_ticket[2]],
                     ['Vehicle No', self.selected_ticket[3]],
                     ['Customer', self.selected_ticket[4]],
                     ['Product', self.selected_ticket[5]],
                     ['Plant No', self.selected_ticket[6]],
                     ['Driver', self.selected_ticket[7]],
                     ['Operator', self.selected_ticket[8]],
                     [self.manager.cx_field_2, self.selected_ticket[10]],
                     ['First Weight', f'{self.selected_ticket[11]} kg'],
                     ['Second Weight', f'{self.selected_ticket[12]} kg'],
                     ['Net Weight', f'{self.selected_ticket[13]}']]
                )
            else:
                ticket.set_ticket_info(
                    [['Ticket No', self.selected_ticket[0]],
                     ['Time-1', self.selected_ticket[1]],
                     ['Time-2', self.selected_ticket[2]],
                     ['Vehicle No', self.selected_ticket[3]],
                     ['Customer', self.selected_ticket[4]],
                     ['Product', self.selected_ticket[5]],
                     ['Plant No', self.selected_ticket[6]],
                     ['Driver', self.selected_ticket[7]],
                     ['Operator', self.selected_ticket[8]],
                     ['First Weight', f'{self.selected_ticket[11]} kg'],
                     ['Second Weight', f'{self.selected_ticket[12]} kg'],
                     ['Net Weight', f'{self.selected_ticket[13]}']]
                )

            ticket.print_docx(1, 2)
            del ticket
            return True

        elif self.manager.printer_format == 'Format-1':
            from sysCom.ticketDoc import TicketFormat1
            ticket = TicketFormat1()
            ticket.set_ticket_info(
                [self.selected_ticket[0],
                 self.selected_ticket[3],
                 f'{self.selected_ticket[11]} kg',
                 f'{self.selected_ticket[12]} kg',
                 self.selected_ticket[1],
                 self.selected_ticket[2],
                 f'{self.selected_ticket[13]}'
                 ]
            )
            ticket.print_docx(1, 2)
            del ticket
            return True

        elif self.manager.printer_format == 'Format-2':
            from sysCom.ticketDoc import TicketFormat2
            ticket = TicketFormat2()
            ticket.set_ticket_info(
                [self.selected_ticket[0],
                 self.selected_ticket[3],
                 f'{self.selected_ticket[11]} kg',
                 f'{self.selected_ticket[12]} kg',
                 self.selected_ticket[1],
                 self.selected_ticket[2],
                 f'{self.selected_ticket[13]}',
                 self.selected_ticket[4],
                 self.selected_ticket[5]]
            )
            ticket.print_docx(1, 2)
            del ticket
            return True
        elif self.manager.printer_format == 'Format-4':
            from sysCom.ticketDoc import TicketFormat4
            ticket = TicketFormat4()
            ticket.set_ticket_info(
                [self.selected_ticket[0],
                 self.selected_ticket[3],
                 f'{self.selected_ticket[11]} kg',
                 f'{self.selected_ticket[12]} kg',
                 self.selected_ticket[1],
                 self.selected_ticket[2],
                 f'{self.selected_ticket[13]}',
                 self.selected_ticket[4],
                 self.selected_ticket[5]]
            )
            ticket.print_docx(1, 2)
            del ticket
            return True
        else:
            return False

    def clear_search(self):

        self.clear_event = True
        self.ids.vehicle_text.text = ''
        self.ids.ticket_text.text = ''
        self.ids.customer_text.text = ''
        self.ids.plant_text.text = ''
        self.ids.driver_text.text = ''
        self.ids.record_select_button.text = '- Select with PgUp or PgDn-'
        self.search_result = [['Please search']]
        self.ids.from_date_text.text = ''
        self.ids.to_date_text.text = ''
        self.ids.show_result_layout.clear_widgets()
        self.selected_ticket = []
        self.current_showing_ticket = 0
        return
