from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class MultiWindow(Screen):

    side_sel_grid = ObjectProperty()
    text_in_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(MultiWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)
        self.edit_text_field = 0
        self.first_time_load = True

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        if self.manager.current == "multi_page" and self.first_time_load:
            self.first_time_load = False
            self.text_field_count = 5 + (1 if self.ids.cx1_text.opacity == 1 else 0) \
                + (1 if self.ids.cx2_text.opacity == 1 else 0)

        if self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "multi_page" and keycode == 43:
            self.text_in_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "multi_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.text_in_grid.focus = True
            return True

        elif ~self.text_in_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "multi_page" and keycode == 43:
            self.text_in_grid.focus = True
            return True

        # arrow key direction
        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "multi_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                print('pg3 save and print fn call here')
            elif button_index == 2:
                print('pg3 save fn call here')
            elif button_index == 1:
                self.ids.vehicle_text.text = ''
                self.ids.ticket_text.text = ''
                self.ids.datetime_text.text = ''
                self.ids.customer_text.text = ''
                self.ids.product_text.text = ''
                self.ids.plant_text.text = ''
                self.ids.driver_text.text = ''
                self.ids.operator_text.text = ''
                self.ids.weight_text.text = ''
                self.ids.cx1_text.text = ''
                self.ids.cx2_text.text = ''
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "main_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            return True

        # keyboard shot-cut
        if 'alt' in modifiers and self.manager.current == "multi_page":
            if text == '1':
                print('page 3 save & print fn from short-cut')

            elif text == '2':
                print('page 3 save fn from short-cut')

            elif text == '3':
                self.ids.vehicle_text.text = ''
                self.ids.ticket_text.text = ''
                self.ids.datetime_text.text = ''
                self.ids.customer_text.text = ''
                self.ids.product_text.text = ''
                self.ids.plant_text.text = ''
                self.ids.driver_text.text = ''
                self.ids.operator_text.text = ''
                self.ids.weight_text.text = ''
                self.ids.cx1_text.text = ''
                self.ids.cx2_text.text = ''

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

        if self.text_in_grid.focus and self.manager.current == "multi_page":
            if keycode == 81:
                if self.edit_text_field < self.text_field_count:
                    self.edit_text_field += 1

            elif keycode == 82:
                if self.edit_text_field > 0:
                    self.edit_text_field -= 1

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

        if self.manager.current != "multi_page":
            # deselect selected nodes
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.text_in_grid.focus = False
            self.side_sel_grid.focus = False

        return
