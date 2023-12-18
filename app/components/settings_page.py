import flet as ft

from components.settings.test_templates import TemplateTest
from components.settings.test_cut_template import TemplateCutTest
from components.buttons import MainButton, RedButton


class Settings:
    def __init__(self, page, master):
        self.page = page
        self.master = master

        out_system = MainButton("В систему", self.shut_down)
        templates_test_button = MainButton("Тест шаблонов", self.setting_tenplate)
        templates_cut_test_button = MainButton("Тест разрезов", self.setting_cut_template)
        back_button = RedButton("Назад", self.back_main)

        self.page.add(
            ft.Column(
                [
                    ft.Row([out_system], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([templates_test_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([templates_cut_test_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=20,
            )
        )

    def back_main(self, e):
        self.master.back_main_page()

    def setting_tenplate(self, e):
        self.master.new_win(TemplateTest)
    
    def setting_cut_template(self, e):
        self.master.new_win(TemplateCutTest)

    def shut_down(self, e):
        self.page.window_destroy()
