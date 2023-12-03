import flet as ft
from components.buttons import MainText
from components.photo_page import PhotoPage

import os


class UserChoise:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.name_category = self.master.session[4]
        self.list_template = [
            name.split(".")[0]
            for name in os.listdir(f"./templates/{self.name_category}")
            if name.split(".")[1] == "png"
        ]
        self.cards = ft.Row(
            wrap=False,
            scroll="AUTO",
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.add(
            ft.Row(
                [
                    ft.Text(
                        self.name_category,
                        style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.add(self.cards)

        for i in self.list_template:
            self.creact_container(i)
            self.page.update()
        
        self.page.update()

    def creact_container(self, name):
        self.cards.controls.append(
            ft.Container(
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                width=620,
                height=922,
                border_radius=15,
                ink=True,
                on_click=lambda e: self.photo_maker(e, name),
                image_src=f"./templates/{self.name_category}/{name}.png",
            )
        )

    def photo_maker(self, e, name):
        self.master.new_win(PhotoPage, name)
