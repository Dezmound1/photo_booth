import os

import flet as ft
from components.buttons import BackButton, MainText, RedButton
from components.print_page import PrintPage

class PhotoHistory:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.dir_photo = self.master.session[3]

        self.index = 1
        self.list_template = os.listdir(f"{self.dir_photo}/photo_templates")
        self.path = f"{self.dir_photo}/photo_templates/"

        self.count_open = 1
        
        self.cards = ft.Row(expand=1, width=1600, scroll="AUTO")
        self.content = ft.Row(
            [
                ft.Row([self.cards], width=1600),
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
        self.page.add(self.content)
        

        for i in self.list_template:
            self.creact_container(i)
            self.page.update()
            
        self.page.update()
        self.page.add(self.buttom_event)
        self.page.add(
            ft.Row(controls=[RedButton("Назад", lambda e: self.back(e))],alignment=ft.MainAxisAlignment.CENTER),
        )
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