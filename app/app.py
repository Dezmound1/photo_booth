import flet as ft
from components.main import Main
from components.user_choise import UserChoise

class Pages:
    def __init__(self, page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.views = None

        self.new_win(Main)

    def new_win(self, class_name_page, params=None):
        if self.views:
            if not params:
                self.page.clean()
                self.views = class_name_page(self.page, self)
            else:
                self.page.clean()
                self.views = class_name_page(self.page, self, params)
        else:
            if not params:
                self.page.clean()
                self.views = class_name_page(self.page, self)
            else:
                self.page.clean()
                self.views = class_name_page(self.page, self, params)

    def back_main_page(self):
        self.page.clean()
        self.views = Main(self.page, self)

    def user_choise(self, name):
        self.page.clean()
        self.views = UserChoise(self.page, self, name)
    
    def back_user_list(self, name):
        self.page.clean()
        self.views = UserChoise(self.page, self, name)


def main(page: ft.Page):
    page.window_full_screen = True
    Pages(page=page)


if __name__ == "__main__":
    ft.app(target=main)
