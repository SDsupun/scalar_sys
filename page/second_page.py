from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from page.sys_popup import SystemPopup


class SecondWindow(Screen):
    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.edit_text_field = 0
        self.first_time_load = True
        self.first_ticket_found = False
        Clock.schedule_interval(self.get_net_weight, 1)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.manager.current == "second_page" and self.first_time_load:
            self.first_time_load = False
            self.text_field_count = 1 + (1 if self.ids.cx1_text.opacity == 1 else 0) \
                + (1 if self.ids.cx2_text.opacity == 1 else 0)

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "second_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "second_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "second_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        # arrow key direction
        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "second_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                save_ok = self.save_ticket_test()
                if save_ok:
                    print_ok = self.print_ticket()
                    if print_ok:
                        SystemPopup(title="Info", notice="Saved & Printing!").open()
                        self.clear_ticket()
                    else:
                        pass
                else:
                    pass
            elif button_index == 2:
                save_ok = self.save_ticket_test()
                if save_ok:
                    SystemPopup(title="Info", notice="Saved!").open()
                    self.clear_ticket()
                else:
                    pass

            elif button_index == 1:
                self.clear_ticket()
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "second_page":
            if text == '1':
                save_ok = self.save_ticket_test()
                if save_ok:
                    print_ok = self.print_ticket()
                    if print_ok:
                        SystemPopup(title="Info", notice="Saved & Printing!").open()
                        self.clear_ticket()
                    else:
                        pass
                else:
                    pass

            elif text == '2':
                save_ok = self.save_ticket_test()
                if save_ok:
                    SystemPopup(title="Info", notice="Saved!").open()
                    self.clear_ticket()
                else:
                    pass

            elif text == '3':
                self.clear_ticket()

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

        if self.text_in_grid.focus and self.manager.current == "second_page":
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
                self.ids.operator_text.focus = True
            elif self.edit_text_field == 2:
                self.ids.cx1_text.focus = True
            elif self.edit_text_field == 3:
                self.ids.cx2_text.focus = True

            return True

        if self.manager.current != "second_page":
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False

        return

    def save_ticket_test(self):
        self.get_first_ticket_info()
        if self.ids.vehicle_text.text == '':
            SystemPopup(title="Warning!", notice="No Data Found!").open()
            return False
        elif not self.first_ticket_found:
            SystemPopup(title="Info", notice="First Weight Not Found!").open()
            return False

        else:
            try:
                second_weight = int(self.ids.second_weight_text.text.split()[0])
            except ValueError:
                SystemPopup(title="Warning!", notice="Device Not Detected!").open()
                return False
            if self.ids.net_weight_text.text == "--":
                SystemPopup(title="Warning!", notice="Net weight calculation error!").open()
                return False

            save_ticket_sql = f'''INSERT INTO scalar_system.second_ticket(
                                                    ticket_no,
                                                    first_datetime,
                                                    second_datetime,
                                                    vehicle_no,
                                                    customer,
                                                    product,
                                                    plant_no,
                                                    driver_name,
                                                    operator_name,
                                                    cx_field_1,
                                                    cx_field_2,
                                                    first_weight,
                                                    second_weight,
                                                    net_weight
                                                ) VALUES(
                                                {self.ids.ticket_text.text},
                                                '{self.ids.datetime_1_text.text}',
                                                '{self.ids.datetime_2_text.text}',
                                                '{self.ids.vehicle_text.text}',
                                                '{self.ids.customer_text.text}', 
                                                '{self.ids.product_text.text}',
                                                '{self.ids.plant_text.text}',
                                                '{self.ids.driver_text.text}',
                                                '{self.ids.operator_text.text}',
                                                '{self.ids.cx1_text.text}', 
                                                '{self.ids.cx2_text.text}',
                                                {self.ids.first_weight_text.text.split()[0]},
                                                {second_weight},
                                                '{self.ids.net_weight_text.text}')'''
            
            try:
                cursor = self.manager.db_conn.cursor()
                cursor.execute(save_ticket_sql)
                cursor.execute('commit')
                self.manager.second_weight_count += 1
                
                # auto back: comment here
                self.manager.transition.direction = "right"
                self.manager.current = "main_page"
                self.manager.page_focus()
                
                return True
            except:
                SystemPopup(title="Warning!", notice="Database Error!").open()
                return False

    def clear_ticket(self):
        self.ids.ticket_text.text = ''
        self.ids.datetime_1_text.text = ''
        self.ids.vehicle_text.text = ''
        self.ids.customer_text.text = ''
        self.ids.product_text.text = ''
        self.ids.plant_text.text = ''
        self.ids.driver_text.text = ''
        self.ids.operator_text.text = ''
        self.ids.first_weight_text.text = ''
        self.ids.net_weight_text.text = '0'
        self.ids.cx1_text.text = ''
        self.ids.cx2_text.text = ''
        return

    def get_net_weight(self, _):
        
        try:
            net_weight = float(self.ids.first_weight_text.text.split()[0]) \
                         - float(self.ids.second_weight_text.text.split()[0])
            net_weight = int(net_weight)
            if net_weight < 0:
                self.ids.net_weight_text.text = f"{abs(net_weight)} kg (out)"
            else:
                self.ids.net_weight_text.text = f"{abs(net_weight)} kg (in)"
        except ValueError:
            self.ids.net_weight_text.text = "--"
        except IndexError:
            self.ids.net_weight_text.text = "--"

        return

    def get_first_ticket_info(self):
        ticket_info_sql = f'''SELECT * FROM 
                                        (SELECT * FROM scalar_system.first_ticket WHERE 
                                        vehicle_no='{self.ids.vehicle_text.text}') a
                                        WHERE a.ticket_no NOT IN
                                        (SELECT ticket_no FROM scalar_system.second_ticket WHERE 
                                        vehicle_no='{self.ids.vehicle_text.text}') '''

        cursor = self.manager.db_conn.cursor()
        cursor.execute(ticket_info_sql)
        self.first_ticket_found = False
        for info in cursor.fetchall():
            self.first_ticket_found = True
            self.ids.ticket_text.text = str(info[0])
            self.ids.datetime_1_text.text = str(info[1])
            self.ids.vehicle_text.text = str(info[2])
            self.ids.customer_text.text = str(info[3])
            self.ids.product_text.text = str(info[4])
            self.ids.plant_text.text = str(info[5])
            self.ids.driver_text.text = str(info[6])
            self.ids.operator_text.text = str(info[7])
            self.ids.first_weight_text.text = f'{info[10]} kg'
            self.ids.cx1_text.text = str(info[8])
            self.ids.cx2_text.text = str(info[9])

        return

    def print_ticket(self):
        if self.ids.vehicle_text.text == '' or not self.ids.second_weight_text.text[0].isdigit():
            SystemPopup(title="Warning!", notice="No Data to Print!").open()
            return False

        if self.manager.cx_field_1_inuse or self.manager.cx_field_2_inuse or self.manager.printer_format == 'Format-3':
            from sysCom.ticketDoc import TicketFormat3
            ticket = TicketFormat3()
            if self.manager.cx_field_1_inuse and self.manager.cx_field_2_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_text.text],
                     ['Time-1', self.ids.datetime_1_text.text],
                     ['Time-2', self.ids.datetime_2_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     [self.manager.cx_field_1, self.ids.cx1_text.text],
                     [self.manager.cx_field_2, self.ids.cx2_text.text],
                     ['Second Weight', self.ids.second_weight_text.text],
                     ['First Weight', self.ids.first_weight_text.text],
                     ['Net Weight', self.ids.net_weight_text.text]]
                )
            elif self.manager.cx_field_1_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_text.text],
                     ['Time-1', self.ids.datetime_1_text.text],
                     ['Time-2', self.ids.datetime_2_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     [self.manager.cx_field_1, self.ids.cx1_text.text],
                     ['Second Weight', self.ids.second_weight_text.text],
                     ['First Weight', self.ids.first_weight_text.text],
                     ['Net Weight', self.ids.net_weight_text.text]]
                )
            elif self.manager.cx_field_2_inuse:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_text.text],
                     ['Time-1', self.ids.datetime_1_text.text],
                     ['Time-2', self.ids.datetime_2_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     [self.manager.cx_field_2, self.ids.cx2_text.text],
                     ['Second Weight', self.ids.second_weight_text.text],
                     ['First Weight', self.ids.first_weight_text.text],
                     ['Net Weight', self.ids.net_weight_text.text]]
                )
            else:
                ticket.set_ticket_info(
                    [['Ticket No', self.ids.ticket_text.text],
                     ['Time-1', self.ids.datetime_1_text.text],
                     ['Time-2', self.ids.datetime_2_text.text],
                     ['Vehicle No', self.ids.vehicle_text.text],
                     ['Customer', self.ids.customer_text.text],
                     ['Product', self.ids.product_text.text],
                     ['Plant No', self.ids.plant_text.text],
                     ['Driver', self.ids.driver_text.text],
                     ['Operator', self.ids.operator_text.text],
                     ['Second Weight', self.ids.second_weight_text.text],
                     ['First Weight', self.ids.first_weight_text.text],
                     ['Net Weight', self.ids.net_weight_text.text]]
                )

            ticket.print_docx(int(self.ids.ticket_text.text), 2)
            del ticket
            return True

        elif self.manager.printer_format == 'Format-1':
            from sysCom.ticketDoc import TicketFormat1
            ticket = TicketFormat1()
            ticket.set_ticket_info(
                [self.ids.ticket_text.text,
                 self.ids.vehicle_text.text,
                 self.ids.first_weight_text.text,
                 self.ids.second_weight_text.text,
                 self.ids.datetime_1_text.text,
                 self.ids.datetime_2_text.text,
                 self.ids.net_weight_text.text
                 ]
            )
            ticket.print_docx(int(self.ids.ticket_text.text), 2)
            del ticket
            return True

        elif self.manager.printer_format == 'Format-2':
            from sysCom.ticketDoc import TicketFormat2
            ticket = TicketFormat2()
            ticket.set_ticket_info(
                [self.ids.ticket_text.text,
                 self.ids.vehicle_text.text,
                 self.ids.first_weight_text.text,
                 self.ids.second_weight_text.text,
                 self.ids.datetime_1_text.text,
                 self.ids.datetime_2_text.text,
                 self.ids.net_weight_text.text,
                 self.ids.customer_text.text,
                 self.ids.product_text.text]
            )
            ticket.print_docx(int(self.ids.ticket_text.text), 2)
            del ticket
            return True
        elif self.manager.printer_format == 'Format-4':
            from sysCom.ticketDoc import TicketFormat4
            ticket = TicketFormat4()
            ticket.set_ticket_info(
                [self.ids.ticket_text.text,
                 self.ids.vehicle_text.text,
                 self.ids.first_weight_text.text,
                 self.ids.second_weight_text.text,
                 self.ids.datetime_1_text.text,
                 self.ids.datetime_2_text.text,
                 self.ids.net_weight_text.text,
                 self.ids.customer_text.text,
                 self.ids.product_text.text]
            )
            ticket.print_docx(int(self.ids.ticket_text.text), 2)
            del ticket
            return True
        else:
            return False

    def lookup(self, column='vehicle_no'):
        if len(self.ids.vehicle_text.text) < 1:
            self.ids.lookup_layout.clear_widgets()
            return
        lookup_sql = f'''SELECT vehicle_no, customer, product, plant_no, driver_name 
            FROM (SELECT * FROM scalar_system.first_ticket WHERE 
                {column} LIKE '{self.ids.vehicle_text.text}%') a
                WHERE a.ticket_no NOT IN
                (SELECT ticket_no FROM scalar_system.second_ticket WHERE 
                {column} LIKE '{self.ids.vehicle_text.text}%') '''

        cursor = self.manager.db_conn.cursor()
        cursor.execute(lookup_sql)
        lookup_heading = ['Vehicle', 'Customer', 'Product', 'Plant', 'Driver']
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
