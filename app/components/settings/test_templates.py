import flet as ft

import os

from components.settings.template_view import TemplateView
from components.buttons import RedButton


class TemplateTest:
    def __init__(self, page, master):
        self.page = page
        self.master = master
        self.list_template = self.get_file_paths()
        self.cards = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self.back_btn = RedButton("Назад", self.back)
        self.page.add(self.back_btn)
        self.page.add(self.cards)
        for i in self.list_template:
            self.creact_container(i)
            self.page.update()

    def get_file_paths(self):
        file_paths = []

        for root, dirs, files in os.walk("./templates"):
            for file in files:
                file_path = os.path.join(root, file)
                file_paths.append(file_path)

        file_paths = [i for i in file_paths if not i.startswith("./templates/test_img")]
        file_paths = [i for i in file_paths if not i.endswith(".json")]

        return file_paths

    def creact_container(self, path):
        self.cards.controls.append(
            ft.Container(
                margin=10,
                padding=10,
                alignment=ft.alignment.center,
                width=620,
                height=922,
                border_radius=15,
                ink=True,
                on_click=lambda e: self.click_photo(e, path),
                image_src=path,
            )
        )
    
    def click_photo(self, e, path):
        self.master.new_win(TemplateView,path)
        
    def back(self, e):
        self.master.back_settings_template()