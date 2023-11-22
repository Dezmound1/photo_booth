import flet as ft
from components.buttons import MainText
from components.photo_page import PhotoPage


class UserChoise:
    def __init__(self, page, master, name):
        self.master = master
        self.page = page
        self.name_category = name
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

        for i in range(5):
            self.cards.controls.append(
                ft.Container(
                    content=MainText(f"CARD {i}"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREY_600,
                    width=420,
                    height=1080,
                    border_radius=15,
                    ink=True,
                    on_click=self.photo_maker,
                )
            )
            self.page.update()

    def photo_maker(self, e):
        self.master.new_win(PhotoPage, self.name_category)
