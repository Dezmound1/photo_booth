import flet as ft
import cups
from PIL import Image

import json

from components.buttons import MainButton, RedButton



class PrintPage:
    def __init__(self, page, master, path_img):
        self.page = page
        self.master = master
        self.path_img = path_img[0]
        self.is_history = path_img[1]
        path = "/mnt/my_vfat_partition/templates/" + self.master.session[4] + "/" + path_img[0].split("/")[-1].split(".")[0].split("_")[0] + ".json"
        self.setting = json.load(open(path))
        self.cut = self.setting.get("ComboPrint")
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
            controls=[MainButton("Печать фото", self.do_nothing)]
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
        self.done_button.controls[0].disabled=True
        img = Image.open(self.path_img)
        width, height = img.size
        
        cut_y = 0
        if self.setting.get("cut_y"):
            cut_y = self.setting.get("cut_y")
            
        cut_x = 0
        if self.setting.get("cut_x"):
            cut_x = self.setting.get("cut_x")
        
        new_width = width + abs(cut_x)
        new_height = height + abs(cut_y)
        new_img = Image.new("RGBA", (new_width, new_height), (0, 0, 0, 0))
        
        x_cut = 0
        if cut_x > -1:
            x_cut = cut_x
        
        y_cut = 0
        if cut_y > -1:
            y_cut = cut_y
            
        new_img.paste(img, (x_cut, y_cut))
        
        new_img.save("./test.png")

        img.close()
        new_img.close()
        
        filename = "./test.png"
        
        for _ in range(int(self.txt_number.value)):
            if self.cut:
                setting = {"copies": "1"}
            else:
                setting = {"copies": "1", 'media': 'custom_104.99x162.56mm_104.99x162.56mm'}
            
            conn = cups.Connection()
            printers = conn.getPrinters()
            for printer in printers:
                conn.printFile(printer, filename, "PhotoBox", setting)
        
        self.master.cur.execute("SELECT num_printed FROM session WHERE id = ?", (self.master.session[0],))
        row = self.master.cur.fetchone()
        if row is not None:
            current_num_printed = row[0]

            # Обновление значения num_printed
            new_num_printed = current_num_printed + int(self.txt_number.value)
            self.master.cur.execute("UPDATE session SET num_printed = ? WHERE id = ?", (new_num_printed, self.master.session[0]))

            # Фиксация изменений
            self.master.conn.commit()
            
        self.back(2)
