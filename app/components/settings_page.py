import flet as ft
from components.buttons import MainButton, MainText, RedButton

class Settings:
    def __init__(self, page, master):
        self.page = page
        self.master = master

        camera_test_button = MainButton('Тест камеры', self.void)
        printer_test_button = MainButton('Тест принтера', self.void)
        back_button = RedButton('Назад', self.back_main)

        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            camera_test_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            printer_test_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        [
                            back_button
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                spacing=20
            )
        )
    def back_main(self, e):
        self.master.back_main_page()

    def void(e):
        print('do_nothing')
    