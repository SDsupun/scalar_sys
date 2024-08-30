from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from mysql import connector

from mysql.connector import OperationalError

from page.sys_popup import SystemPopup
from sysCom.ticketDoc import TicketFormat1, TicketFormat3, TicketFormat2, TicketFormat4


class FirstWindow(Screen):

    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()
    first_weight_text = ObjectProperty()

    def __init__(self, **kwargs):
        super(FirstWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.edit_text_field = 0
        self.first_time_load = True
        self.incomplete_ticket_found = False

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.manager.current == "first_page" and self.first_time_load:
            self.first_time_load = False
            self.text_field_count = 5 + (1 if self.ids.cx1_text.opacity == 1 else 0) \
                + (1 if self.ids.cx2_text.opacity == 1 else 0)

        if self.text_in_grid.focus and ~self.side_sel_grid.focus\
                and self.manager.current == "first_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "first_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "first_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        # arrow key direction
        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "first_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                save_ok = self.save_ticket_test()
                if save_ok:
                    self.update_lookup()
                    print_ok = self.print_ticket()
                    if print_ok:
                        SystemPopup(title="Info", notice="Saved and Printing Ticket!").open()
                        self.clear_ticket()
                    else:
                        pass
                else:
                    pass

                return True

            elif button_index == 2:
                save_ok = self.save_ticket_test()
                if save_ok:
                    self.update_lookup()
                    self.clear_ticket()
                    SystemPopup(title="Info", notice="Saved Ticket!").open()
                else:
                    pass
                return True

            elif button_index == 1:
                self.clear_ticket()
                return True

            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True
                return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "first_page":
            if text == '1':
                save_ok = self.save_ticket_test()
                if save_ok:
                    self.update_lookup()
                    print_ok = self.print_ticket()
                    if print_ok:
                        SystemPopup(title="Info", notice="Saved and Printing Ticket!").open()
                        self.clear_ticket()
                    else:
                        pass
                else:
                    pass

                return True

            elif text == '2':
                save_ok = self.save_ticket_test()
                if save_ok:
                    self.update_lookup()
                    self.clear_ticket()
                    SystemPopup(title="Info", notice="Saved Ticket!").open()
                else:
                    pass
                return True

            elif text == '3':
                self.clear_ticket()
                return True

            elif text == '4':
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.back_key = True
                return True

            elif text == '0':
                self.manager.transition.direction = "left"
                self.manager.current = "login_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.back_key = True
                return True

        if self.text_in_grid.focus and self.manager.current == "first_page":
            if keycode == 81:
                if self.edit_text_field < self.text_field_count:
                    self.edit_text_field += 1

            elif keycode == 82:
                if self.edit_text_field > 0:
                    self.edit_text_field -= 1
            else:
                return False

            if self.edit_text_field == 0:
                self.ids.vehicle_text.focus = True
            elif self.edit_text_field == 1:
                self.ids.customer_text.focus = True
            elif self.edit_text_field == 2:
                self.ids.product_text.focus = True
            elif self.edit_text_field == 3:
                self.ids.plant_text.focus = True
            elif self.edit_text_field == 4:
                self.ids.driver_text.focus = True
            elif self.edit_text_field == 5:
                self.ids.operator_text.focus = True
            elif self.edit_text_field == 6:
                self.ids.cx1_text.focus = True
            elif self.edit_text_field == 7:
                self.ids.cx2_text.focus = True
            return True

        if self.manager.current != "first_page":
            self.edit_text_field = 0
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False

    def get_ticket(self):
        ticket_no_sql = '''SELECT DISTINCT ticket_no FROM scalar_system.first_ticket 
            ORDER BY ticket_no DESC LIMIT 1;'''
        try:
            cursor = self.manager.db_conn.cursor()
            cursor.execute(ticket_no_sql)
            ticket_no = 0
            for tk in cursor.fetchall():
                ticket_no = tk[0]
            ticket_no += 1
            return str(ticket_no)
        except OperationalError:
            return '- No Connection -'

    def save_ticket_test(self):
        if self.ids.vehicle_text.text == '':
            SystemPopup(title="Warning!", notice="No Data to Save!").open()
            return False
        elif self.incomplete_ticket_found:
            SystemPopup(title="Warning!", notice="Pending Second Weight Found.").open()
            return False
        else:
            try:
                first_weight = float(self.ids.first_weight_text.text.split()[0])
            except ValueError:
                SystemPopup(title="Warning!", notice="Device Not Connected!").open()
                return False
            save_ticket_sql = f'''INSERT INTO scalar_system.first_ticket(
                                                    ticket_no,
                                                    first_datetime,
                                                    vehicle_no,
                                                    customer,
                                                    product,
                                                    plant_no,
                                                    driver_name,
                                                    operator_name,
                                                    cx_field_1,
                                                    cx_field_2,
                                                    first_weight
                                                ) VALUES(
                                                {self.ids.ticket_no_text.text},
                                                '{self.ids.datetime_text.text}',
                                                '{self.ids.vehicle_text.text}',
                                                '{self.ids.customer_text.text}', 
                                                '{self.ids.product_text.text}',
                                                '{self.ids.plant_text.text}',
                                                '{self.ids.driver_text.text}',
                                                '{self.ids.operator_text.text}',
                                                '{self.ids.cx1_text.text}', 
                                                '{self.ids.cx2_text.text}',
                                                {first_weight})'''
            try:
                cursor = self.manager.db_conn.cursor()
                cursor.execute(save_ticket_sql)
                cursor.execute('commit')
                self.manager.first_weight_count += 1
                
                # auto back: comment here
                self.manager.transition.direction = "right"
                self.manager.current = "main_page"
                self.manager.page_focus()
                
                return True
            except:
                SystemPopup(title="Warning!", notice="Database Error!").open()
                return False

    def clear_ticket(self):
        self.ids.ticket_no_text.text = self.get_ticket()
        self.ids.vehicle_text.text = ''
        self.ids.customer_text.text = ''
        self.ids.product_text.text = ''
        self.ids.plant_text.text = ''
        self.ids.driver_text.text = ''
        self.ids.operator_text.text = ''
        self.ids.cx1_text.text = ''
        self.ids.cx2_text.text = ''
        return

    def check_incomplete_ticket(self):
        ticket_info_sql = f'''SELECT * FROM 
                                                (SELECT * FROM scalar_system.first_ticket WHERE 
                                                vehicle_no='{self.ids.vehicle_text.text}') a
                                                WHERE a.ticket_no NOT IN
                                                (SELECT ticket_no FROM scalar_system.second_ticket WHERE 
                                                vehicle_no='{self.ids.vehicle_text.text}') '''
        cursor = self.manager.db_conn.cursor()
        cursor.execute(ticket_info_sql)
        self.incomplete_ticket_found = False
        for tk in cursor.fetchall():
            self.incomplete_ticket_found = True

        return

    def print_ticket(self):

        if self.ids.vehicle_text.text == '' or not self.ids.first_weight_text.text[0].isdigit():
            SystemPopup(title="Warning!", notice="No Data to Print!").open()
            return False
        if self.manager.cx_field_1_inuse or self.manager.cx_field_2_inuse or self.manager.printer_format == 'Format-3':
            ticket = TicketFormat3()
            if self.manager.cx_field_1_inuse and self.manager.cx_field_2_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_no_text.text],
                     ['Time', self.ids.datetime_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     [self.manager.cx_field_1, self.ids.cx1_text.text],
                     [self.manager.cx_field_2, self.ids.cx2_text.text],
                     ['First Weight', self.ids.first_weight_text.text]]
                )
            elif self.manager.cx_field_1_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_no_text.text],
                     ['Time', self.ids.datetime_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     [self.manager.cx_field_1, self.ids.cx1_text.text],
                     ['First Weight', self.ids.first_weight_text.text]]
                )
            elif self.manager.cx_field_2_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_no_text.text],
                     ['Time', self.ids.datetime_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     [self.manager.cx_field_2, self.ids.cx2_text.text],
                     ['First Weight', self.ids.first_weight_text.text]]
                )
            else:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_no_text.text],
                     ['Time', self.ids.datetime_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     ['First Weight', self.ids.first_weight_text.text]]
                )

            ticket.print_docx(int(self.ids.ticket_no_text.text), 1)
            del ticket
            return True

        elif self.manager.printer_format == 'Format-1':
            ticket = TicketFormat1()
            ticket.set_ticket_info(
                [self.ids.ticket_no_text.text,
                 self.ids.vehicle_text.text,
                 self.ids.first_weight_text.text,
                 '-',
                 self.ids.datetime_text.text,
                 '-',
                 '-'
                 ]
            )
            ticket.print_docx(int(self.ids.ticket_no_text.text), 1)
            del ticket
            return True

        elif self.manager.printer_format == 'Format-2':
            ticket = TicketFormat2()
            ticket.set_ticket_info(
                [self.ids.ticket_no_text.text,
                 self.ids.vehicle_text.text,
                 self.ids.first_weight_text.text,
                 '-',
                 self.ids.datetime_text.text,
                 '-',
                 '-',
                 self.ids.customer_text.text,
                 self.ids.product_text.text]
            )
            ticket.print_docx(int(self.ids.ticket_no_text.text), 1)
            del ticket
            return True
        elif self.manager.printer_format == 'Format-4':
            ticket = TicketFormat4()
            ticket.set_ticket_info(
                [self.ids.ticket_no_text.text,
                 self.ids.vehicle_text.text,
                 self.ids.first_weight_text.text,
                 '-',
                 self.ids.datetime_text.text,
                 '-',
                 '-',
                 self.ids.customer_text.text,
                 self.ids.product_text.text]
            )
            ticket.print_docx(int(self.ids.ticket_no_text.text), 1)
            del ticket
            return True
        else:
            return False

    def lookup(self, column='vehicle_no'):
        if len(self.ids.vehicle_text.text) < 3:
            self.ids.lookup_layout.clear_widgets()
            return
        lookup_sql = f'''SELECT * FROM scalar_system.first_lookup 
            WHERE {column} LIKE '{self.ids.vehicle_text.text}%' '''

        cursor = self.manager.db_conn.cursor()
        cursor.execute(lookup_sql)
        lookup_heading = ['Vehicle', 'Customer', 'Product', 'Plant', 'Driver', 'Operator']
        self.ids.lookup_layout.clear_widgets()
        for w in lookup_heading:
            label = Label(text=w, color=(0, 0, 0, 1), size_hint_x=None, width=100)
            label.font_size = label.height * 0.2
            self.ids.lookup_layout.add_widget(label)

        for w in cursor.fetchall():
            for i in w:
                label = Label(text=i, color=(0, 0, 0, 1))
                label.font_size = label.height * 0.2
                self.ids.lookup_layout.add_widget(label)

        return

    def update_lookup(self):
        update_lookup_sql = f'''REPLACE INTO scalar_system.first_lookup SET
            vehicle_no='{self.ids.vehicle_text.text}',
            customer='{self.ids.customer_text.text}',
            product='{self.ids.product_text.text}',
            plant_no='{self.ids.plant_text.text}',
            driver='{self.ids.driver_text.text}',
            operator='{self.ids.operator_text.text}'
        '''
        cursor = self.manager.db_conn.cursor()
        cursor.execute(update_lookup_sql)
        cursor.execute('commit')
        return

    #####chum start
    def get_ticket_no(self):
        ticket_no = ''
        try:
            conn = connector.connect(host="localhost", user="root", password="", database="scalar_system")
            ticket_no_db = "SELECT `Get_Nxt_Ticket_No`()"
            cursor = conn.cursor()
            cursor.execute(ticket_no_db)
            ticket_no = 'test1'
            for pw in cursor.fetchall():
                ticket_no = str(pw[0])
        except:
            ticket_no = ''

        return ticket_no

    def save_ticket( self, ticketNo, dateTime, vechleNo, customerNo, productNo, plantNo, driverNo, operator):
        try:
            conn = connector.connect(host="localhost", user="root", password="", database="scalar_system")
            sql_statement = "CALL `Save_First_Weight`(%s, %s, %s, %s, %s, %s, %s, %s, %f, %s);"
            cursor = conn.cursor()
            cursor.execute(sql_statement, (ticketNo, dateTime, vechleNo, customerNo, productNo, plantNo, driverNo, operator, ))
            ticket_no = 'test1'
            for pw in cursor.fetchall():
                ticket_no = str(pw[0])
        except:
            print('execption save_ticket')

    #####chum end
