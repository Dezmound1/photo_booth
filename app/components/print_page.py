import flet as ft
from components.buttons import MainButton, RedButton
from time import sleep
import cups


class PrintPage:
    def __init__(self, page, master, path_img):
        self.page = page
        self.master = master
        self.path_img = path_img[0]
        self.is_history = path_img[1]
        self.name_category = self.master.session[4]
        
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
                    image_src=self.path_img,
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
        if self.is_history:
            self.master.back_photo_history()
        else:
            self.master.user_choise()

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
        filename = self.path_img
	
        conn = cups.Connection()
        printers = conn.getPrinters()
        for printer in printers:
            conn.printFile(printer, filename, "PhotoBox", {"copies": f"{int(self.txt_number.value)}"})
            
        self.back(2)