import os

import flet as ft
from components.buttons import BackButton, MainText
from components.print_page import PrintPage


class PhotoHistory:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.dir_photo = self.master.session[3]

        self.name_list = os.listdir(f"{self.dir_photo}/photo_templates")
        self.path = f"{self.dir_photo}/photo_templates/"

        self.button_back = BackButton("Назад", self.back)
        self.page.add(
            ft.Row(
                [self.button_back],
                alignment=ft.MainAxisAlignment.START,
                visible=True,
            )
        )

        self.row = ft.GridView(expand=True, runs_count=4)
        self.page.add(self.row)
        for i in self.name_list:
            self.row.controls.append(self.creat_buttom(i))
        self.page.update()

    def creat_buttom(self, name):
        return ft.Container(
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            width=200,
            height=200,
            border_radius=10,
            ink=True,
            on_click=lambda e: self.photo_print(e, name),
            image_src=self.path + name,
        )

    def photo_print(self, e, name):
        path_phoro = self.path + name
        self.master.new_win(PrintPage, (path_phoro, True))

    def back(self, e):
        self.master.back_settings()
