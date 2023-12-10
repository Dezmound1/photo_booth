import flet as ft

from components.settings.test_templates import TemplateTest
from components.buttons import MainButton, RedButton


class Settings:
    def __init__(self, page, master):
        self.page = page
        self.master = master

        out_system = MainButton("В систему", self.shut_down)
        camera_test_button = MainButton("Тест камеры", self.void_def)
        printer_test_button = MainButton("Тест принтера", self.void_def)
        templates_test_button = MainButton("Тест шаблонов", self.setting_tenplate)
        back_button = RedButton("Назад", self.back_main)

        self.page.add(
            ft.Column(
                [
                    ft.Row([out_system], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([camera_test_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([printer_test_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([templates_test_button], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Row([back_button], alignment=ft.MainAxisAlignment.CENTER),
                ],
                spacing=20,
            )
        )

    def back_main(self, e):
        self.master.back_main_page()

    def void_def(self, e):
        print("do_nothing")

    def setting_tenplate(self, e):
        self.master.new_win(TemplateTest)

    def shut_down(self, e):
        self.page.window_destroy()
