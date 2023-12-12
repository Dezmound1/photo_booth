import flet as ft
import sqlite3
import cups

import time
import threading

from components.main import Main
from components.user_choise import UserChoise
from components.history import HistoryPage
from components.photo_history import PhotoHistory
from components.settings_page import Settings
from components.settings.test_templates import TemplateTest
from components.page_preview import PreviewsPage


def get_total_active_jobs():
    conn = cups.Connection()
    printers = conn.getPrinters()

    total_jobs = 0

    for printer_name in printers:
        total_jobs += len(conn.getJobs().keys())

    return total_jobs


class Pages:
    def __init__(self, page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.views = None
        self.conn = sqlite3.connect("./base.db", check_same_thread=False)
        self.cur = self.conn.cursor()

        self.session = None
        page.banner = ft.Container(
            border_radius=30,
            width=70,
            height=70,
            bgcolor=ft.colors.RED,
            opacity=0.5,
        )

        thread = threading.Thread(target=self.check_jobs)
        thread.daemon = True
        thread.start()

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

    def back_settings_template(self):
        self.page.clean()
        self.views = Settings(self.page, self)

    def back_settings_template_all(self):
        self.page.clean()
        self.views = TemplateTest(self.page, self)

    def back_photo_history(self):
        self.page.clean()
        self.views = PhotoHistory(self.page, self)

    def close_banner(self, e):
        self.page.banner.visible = False
        self.page.update()

    def show_banner_click(self, e):
        self.page.banner.visible = True
        self.page.update()

    def check_jobs(self):
        while True:
            total_jobs = get_total_active_jobs()
            if total_jobs > 0:
                self.page.banner.visible = True
                self.page.banner.content = ft.Text(
                    f"{total_jobs}",
                    color="white",
                    size=40,
                    weight="bold",
                    text_align="center",
                )
                self.page.update()
            else:
                self.page.banner.visible = False
                self.page.banner.content = ft.Text(
                    f"{total_jobs}",
                    color="white",
                    size=40,
                    weight="bold",
                    text_align="center",
                )
                self.page.update()
            time.sleep(1)

    def go_camera_main(self):
        self.page.clean()
        self.views = PreviewsPage(self.page, self)


def main(page: ft.Page):
    page.window_full_screen = True
    Pages(page=page)


if __name__ == "__main__":
    ft.app(target=main)
