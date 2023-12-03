import flet as ft
import sqlite3

from components.main import Main
from components.user_choise import UserChoise
from components.history import HistoryPage
from components.photo_history import PhotoHistory

class Pages:
    def __init__(self, page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.views = None
        self.conn = sqlite3.connect("./base.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        
        self.session = None

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

    def user_choise(self):
        self.page.clean()
        self.views = UserChoise(self.page, self)

    def back_settings(self):
        self.page.clean()
        self.views = HistoryPage(self.page, self)
    
    def back_photo_history(self):
        self.page.clean()
        self.views = PhotoHistory(self.page, self)


def main(page: ft.Page):
    page.window_full_screen = True
    Pages(page=page)


if __name__ == "__main__":
    ft.app(target=main)
