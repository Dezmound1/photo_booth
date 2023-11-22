import flet as ft


class PrintPage:
    def __init__(self, page, master):
        self.page = page
        self.master = master
        page.title = "Print your photo"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.txt_number = ft.TextField(value="0", text_align="right", width=400, text_size=30)

        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                border_radius=8,
                                padding=5,
                                width=420,
                                height=700,
                                bgcolor=ft.colors.BLACK,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
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
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            )
        )

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
