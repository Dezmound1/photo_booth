import flet as ft
from components.buttons import MainButton
from components.print_page import PrintPage


class PhotoPage:
    def __init__(self, page, master, name):
        self.page = page
        self.master = master
        self.count = 1
        self.name_category = name

        self.button = MainButton("Создать", self.void)
        self.colum = ft.Column(
            controls=[
                ft.Text(
                    value="YOUR PHOTO",
                    size=40,
                    font_family="RobotoSlab",
                    weight=ft.FontWeight.W_600,
                ),
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.add(
            ft.Row(
                [
                    self.colum,
                    self.button,
                    ft.Column(controls=[MainButton("Назад", lambda e: self.back(e, self.name_category))]),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        )

    def void(self, e):
        if self.count < 5:
            self.count += 1
            self.colum.controls.append(
                ft.Container(
                    ft.Stack(
                        [
                            ft.Container(
                                margin=10,
                                right=0,
                                border_radius=5,
                                width=70,
                                height=70,
                                content=ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="pink600",
                                    icon_size=40,
                                    tooltip="Удалить фотографию",
                                ),
                            )
                        ]
                    ),
                    border_radius=8,
                    padding=5,
                    width=400,
                    height=250,
                    bgcolor=ft.colors.BLACK,
                )
            )
            self.page.update()
        else:
            self.button.visible = False
            self.page.controls[0].controls[1] = MainButton("Сформировать", on_click=self.to_print)
            self.page.update()
            # self.page.add()

    def back(self, e, name):
        self.master.user_choise(name)

    def to_print(self, e):
        self.master.new_win(PrintPage, self.name_category)
