from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen


class MainWindow(Screen):

    main_sel_grid = ObjectProperty()
    side_sel_grid = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):

        # stop executing previous page command
        if self.manager.back_key and self.manager.current == "main_page":
            self.manager.back_key = False
            return False
        if self.main_sel_grid.focus and ~self.side_sel_grid.focus\
                and self.manager.current == "main_page" and keycode == 43:
            if len(self.main_sel_grid.selected_nodes) > 0:
                for node in self.main_sel_grid.selected_nodes:
                    self.main_sel_grid.deselect_node(node)
            self.main_sel_grid.focus = False
            self.side_sel_grid.focus = True
            return True

        elif ~self.main_sel_grid.focus and self.side_sel_grid.focus \
                and self.manager.current == "main_page" and keycode == 43:
            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)
            self.side_sel_grid.focus = False
            self.main_sel_grid.focus = True
            return True

        elif ~self.main_sel_grid.focus and ~self.side_sel_grid.focus \
                and self.manager.current == "main_page" and keycode == 43:
            self.main_sel_grid.focus = True
            return True

        # arrow and enter for direction
        if keycode == 40 and self.side_sel_grid.focus and self.manager.current == "main_page":
            try:
                button_index = self.side_sel_grid.get_selectable_nodes().index(self.side_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 3:
                self.manager.transition.direction = "left"
                self.manager.current = "report_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                return True
            elif button_index == 2:
                self.manager.transition.direction = "left"
                self.manager.current = "print_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                return True
            elif button_index == 1:
                if self.ids.main_setting_button.disabled:
                    return True
                else:
                    self.manager.transition.direction = "left"
                    self.manager.current = "profile_setting_page"
                    self.manager.page_focus()
                    self.manager.transition.direction = "right"
                    return True
            elif button_index == 0:
                self.manager.transition.direction = "left"
                self.manager.current = "login_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True
                return True
            else:
                return False

        # arrow and enter for direction
        if keycode == 40 and self.main_sel_grid.focus and self.manager.current == "main_page":
            try:
                button_index = self.main_sel_grid.get_selectable_nodes().index(self.main_sel_grid.selected_nodes[0])
            except IndexError:
                button_index = -1
            if button_index == 1:
                self.manager.transition.direction = "right"
                self.manager.current = "first_page"
                self.manager.page_focus()
                self.manager.transition.direction = "left"
                return True
            elif button_index == 0:
                self.manager.transition.direction = "right"
                self.manager.current = "second_page"
                self.manager.page_focus()
                self.manager.transition.direction = "left"
                return True
## multipage removed change button_index if adding again
#            elif button_index == 0:
#                self.manager.transition.direction = "right"
#                self.manager.current = "multi_page"
#                self.manager.page_focus()
#                self.manager.transition.direction = "left"
#                return True
            else:
                return False

        # key-shortcut main menu
        if 'ctrl' in modifiers and self.manager.current == "main_page":
            if text == '1':
                self.manager.back_key = True
                self.manager.transition.direction = "right"
                self.manager.current = "first_page"
                self.manager.page_focus()
                self.manager.transition.direction = "left"

            elif text == '2':
                self.manager.back_key = True
                self.manager.transition.direction = "right"
                self.manager.current = "second_page"
                self.manager.page_focus()
                self.manager.transition.direction = "left"

#            elif text == '3':
#                self.manager.back_key = True
#                self.manager.transition.direction = "right"
#                self.manager.current = "multi_page"
#                self.manager.page_focus()
#                self.manager.transition.direction = "left"
            return True

        # key-shortcut side bar
        if 'alt' in modifiers and self.manager.current == "main_page":
            if text == '1':
                self.manager.transition.direction = "left"
                self.manager.current = "report_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '2':
                self.manager.transition.direction = "left"
                self.manager.current = "print_page"
                self.manager.page_focus()
                self.manager.transition.direction = "right"
                self.manager.back_key = True

            elif text == '3':
                if self.ids.main_setting_button.disabled:
                    pass
                else:
                    self.manager.transition.direction = "left"
                    self.manager.current = "profile_setting_page"
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

        # disable focus
        if self.manager.current != "main_page":
            # deselect selected nodes
            if len(self.main_sel_grid.selected_nodes) > 0:
                for node in self.main_sel_grid.selected_nodes:
                    self.main_sel_grid.deselect_node(node)

            if len(self.side_sel_grid.selected_nodes) > 0:
                for node in self.side_sel_grid.selected_nodes:
                    self.side_sel_grid.deselect_node(node)

            self.main_sel_grid.focus = False
            self.side_sel_grid.focus = False

        return
