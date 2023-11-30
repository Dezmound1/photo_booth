import flet as ft
from components.buttons import MainButton, RedButton
from time import sleep


class PrintPage:
    def __init__(self, page, master, name):
        self.page = page
        self.master = master
        self.name_category = name
        page.title = "Print your photo"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.txt_number = ft.TextField(
            value="0", text_align="right", width=400, text_size=30
        )
        self.void_column = ft.Column(
            controls=[
                ft.Text(
                    value="Вы прекрасны",
                    size=37,
                    font_family="RobotoSlab",
                    weight=ft.FontWeight.W_600,
                ),
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
        )

        self.row_preset = ft.Row(
            [
                ft.Container(
                    border_radius=8,
                    padding=5,
                    width=420,
                    height=700,
                    bgcolor=ft.colors.BLACK,
                ),
            ]
        )

        self.row_score = ft.Row(
            [
                ft.IconButton(
                    ft.icons.REMOVE,
                    on_click=self.minus_click,
                    icon_size=50,
                ),
                self.txt_number,
                ft.IconButton(
                    ft.icons.ADD,
                    on_click=self.plus_click,
                    icon_size=50,
                ),
            ]
        )
        self.done_button = ft.Column(
            controls=[MainButton("Распечатать", self.do_nothing)]
        )

        self.page.add(
            ft.Row(
                [
                    self.void_column,
                    self.row_preset,
                    ft.Column(controls=[RedButton("Назад", self.back)]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            ft.Row(
                [
                    self.row_score
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            ),
            ft.Row(
                [
                    self.done_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            )
        )


    def back(self, e):
        self.master.back_user_list(self.name_category)

    def minus_click(self, e):
        if self.txt_number.value == "0":
            self.txt_number.value = "0"
        else:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
            self.page.update()

    def plus_click(self, e):
        if self.txt_number.value == "8":
            self.txt_number.value = "8"
        else:
            self.txt_number.value = str(int(self.txt_number.value) + 1)
            self.page.update()

    def do_nothing(self, e):
        print(f"Вы распечатаете {self.txt_number.value} копий")
        self.master.back_user_list(self.name_category)