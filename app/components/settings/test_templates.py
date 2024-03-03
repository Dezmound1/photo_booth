import flet as ft

import os

from components.settings.template_view import TemplateView
from components.buttons import RedButton
from components.const import PathEnum


class TemplateTest:
    def __init__(self, page, master):
        self.page = page
        self.master = master
        ft.ScrollbarTheme(radius=12)
        self.count_open = 1
        self.index = 1
        self.list_template = self.get_file_paths()
        self.cards = ft.Row(expand=1, width=1200, scroll="AUTO")
        self.content = ft.Row(
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
        self.back_btn = RedButton("Назад", self.back)
        
        
        for i in self.list_template:
            self.creact_container(i)
            self.page.update()
            
        content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Выберите шаблон",
                            style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.content,
                self.buttom_event,
                ft.Row(controls=[RedButton("Назад", lambda e: self.back(e))], alignment=ft.MainAxisAlignment.CENTER),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        
        self.page.add(
            ft.Container(
                image_src="./img/bg.png",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                content=content,
                alignment=ft.alignment.center,
            )
        )

    def get_file_paths(self):
        file_paths = []

        for root, dirs, files in os.walk(PathEnum.mnt_path.value):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

        file_paths = [i for i in file_paths if not i.startswith(f"{PathEnum.mnt_path.value}/test_img")]
        file_paths = [i for i in file_paths if not i.endswith(".json")]

        return file_paths

    def creact_container(self, path):
        i = self.index
        self.cards.controls.append(
            ft.Container(
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                width=320,
                height=622,
                border_radius=15,
                on_click=lambda e: self.click_photo(e, path),
                image_src=path,
                key=f"{i}",
            )
        )
        self.index += 1

    def click_photo(self, e, path):
        self.master.new_win(TemplateView, path)

    def back(self, e):
        self.master.back_settings_template()

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
