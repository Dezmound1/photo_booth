import os

import flet as ft
from components.buttons import BackButton, MainText, RedButton, MainButton
from components.print_page import PrintPage


class PhotoHistory:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.dir_photo = self.master.session[3]

        self.index = 1
        self.list_template_dir = os.listdir(f"{self.dir_photo}/photo_templates")
        self.dir_activite = "dir_0"
        self.list_template = os.listdir(f"{self.dir_photo}/photo_templates/{self.dir_activite}")
        self.path = f"{self.dir_photo}/photo_templates/{self.dir_activite}/"

        self.count_open = 1
        self.cards = ft.Row(expand=1, width=1200, scroll="AUTO")
        self.cards_row = ft.Row(
            [
                ft.Row([self.cards], width=1200),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.buttom_event = ft.Row(
            [
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=self.mun_2),
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_ARROW_LEFT, on_click=self.mun_1),
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_ARROW_RIGHT, on_click=self.add_1),
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click=self.add_2),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )

        content = ft.Column(
            [
                ft.Row(
                    [self.creat_button_dir(i) for i in self.list_template_dir],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.cards_row,
                self.buttom_event,
                ft.Row(
                    controls=[RedButton("Назад", lambda e: self.back(e))], alignment=ft.MainAxisAlignment.CENTER
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        self.creact_slider(self.list_template)
        self.page.update()

        self.page.add(
            ft.Container(
                image_src="./img/bg.png",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                content=content,
                alignment=ft.alignment.center,
            )
        )

        self.page.update()

    def creat_button_dir(self, name):
        return MainButton(name, lambda e: self.update_slider(name))

    def update_slider(self, name_dir):
        self.index = 1
        self.dir_activite = name_dir
        self.list_template = os.listdir(f"{self.dir_photo}/photo_templates/{self.dir_activite}")
        self.path = f"{self.dir_photo}/photo_templates/{self.dir_activite}/"
        self.count_open = 1
        self.creact_slider(self.list_template)

    def creact_slider(self, list_photo_name):
        self.cards.controls = []
        self.page.update()

        for i in list_photo_name:
            self.creact_container(i)
            self.page.update()

    def creact_container(self, name):
        i = self.index
        self.cards.controls.append(
            ft.ElevatedButton(
                content=ft.Image(
                    src=self.path + name,
                    width=320,
                    height=622,
                ),
                key=str(i),
                on_click=lambda e: self.photo_print(e, name),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            )
        )

        self.index += 1

    def photo_print(self, e, name):
        path_phoro = self.path + name
        self.master.new_win(PrintPage, (path_phoro, True))

    def back(self, e):
        self.master.back_settings()

    def add_1(self, e):
        if self.count_open + 1 < self.index:
            self.count_open += 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

    def add_2(self, e):
        if self.count_open + 2 < self.index:
            self.count_open += 2
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

        elif self.count_open + 1 < self.index:
            self.count_open += 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

    def mun_1(self, e):
        if self.count_open - 1 > 0:
            self.count_open -= 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

    def mun_2(self, e):
        if self.count_open - 2 > 0:
            self.count_open -= 2
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

        elif self.count_open - 1 > 0:
            self.count_open -= 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)
