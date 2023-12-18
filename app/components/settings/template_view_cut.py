import flet as ft
from PIL import Image
import cups

import json
import base64
from io import BytesIO

from components.buttons import BackButton
from components.buttons import MainButton


class TemplateViewCut:
    def __init__(self, page, master, path_img):
        self.page = page
        self.page.scroll = "ALWAYS"
        self.master = master
        self.path_img = path_img
        self.settings_path = self.path_img.replace(".png", ".json")
        with open(self.settings_path, "r") as file:
            self.setting_template = json.load(file)
        
        self.cut = self.setting_template.get("ComboPrint")

        self.replace = None
        self.back_btn = BackButton("Назад", on_click=self.back)
        self.container = ft.Container(
            content=self.back_btn,
            alignment=ft.alignment.top_left,
            width=150,
            height=40,
        )
        self.page.add(self.container)

        self.row_preset = ft.Image(
            src_base64="",
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        self.overlay_images(1)

        self.settings = ft.Row(
            wrap=True,
            run_spacing=1,
            width=700,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.settings.controls = [self.creact_setting(0)]
        self.settings.controls.append(
            ft.Row(
                [
                    MainButton("Просмотреть", self.print_img),
                    MainButton("Сохранить", self.save_setting),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                width=600,
                height=80,
            )
        )
        self.page.add(ft.Row([self.row_preset, self.settings]))
        self.page.update()

    def save_setting(self, e):
        with open(self.settings_path, "w") as json_file:
            # Используете метод dump для записи данных в файл
            json.dump(self.setting_template, json_file)

        self.back(1)

    def creact_setting(self, i):
        return ft.Column(
            [
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(
                                    ft.icons.ARROW_DROP_UP,
                                    on_click=lambda e: self.plus_click(e, 1, i),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=270,
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    ft.icons.ARROW_LEFT,
                                    on_click=lambda e: self.minus_click(e, 2, i),
                                ),
                                ft.TextField(
                                    value="0",
                                    text_align=ft.TextAlign.RIGHT,
                                    width=80,
                                ),
                                ft.TextField(
                                    value="0",
                                    text_align=ft.TextAlign.RIGHT,
                                    width=80,
                                ),
                                ft.IconButton(
                                    ft.icons.ARROW_RIGHT,
                                    on_click=lambda e: self.plus_click(e, 2, i),
                                ),
                            ],
                        ),
                        ft.Row(
                            [
                                ft.IconButton(
                                    ft.icons.ARROW_DROP_DOWN,
                                    on_click=lambda e: self.minus_click(e, 1, i),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            width=270,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=1,
            tight=True,
        )

    def minus_click(self, e, num, index):
        self.settings.controls[index].controls[0].controls[1].controls[num].value = str(
            int(self.settings.controls[index].controls[0].controls[1].controls[num].value) - 1
        )
        if num == 1:
            self.setting_template["cut_y"] = int(self.settings.controls[index].controls[0].controls[1].controls[num].value)
        else:
            self.setting_template["cut_x"] = int(self.settings.controls[index].controls[0].controls[1].controls[num].value)

        self.setting_template["Photos"][index]
        self.page.update()

    def plus_click(self, e, num, index):
        self.settings.controls[index].controls[0].controls[1].controls[num].value = str(
            int(self.settings.controls[index].controls[0].controls[1].controls[num].value) + 1
        )
        if num == 1:
            self.setting_template["cut_y"] = int(self.settings.controls[index].controls[0].controls[1].controls[num].value)
        else:
            self.setting_template["cut_x"] = int(self.settings.controls[index].controls[0].controls[1].controls[num].value)

        self.page.update()
        
    def print_img(self, e):
        img = Image.open(self.path_img)
        width, height = img.size
        
        cut_y = 0
        if self.setting_template.get("cut_y"):
            cut_y = self.setting_template.get("cut_y")
            
        cut_x = 0
        if self.setting_template.get("cut_x"):
            cut_x = self.setting_template.get("cut_x")
        
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
        if self.cut:
            setting = {"copies": "1"}
        else:
            setting = {"copies": "1", 'media': 'custom_104.99x162.56mm_104.99x162.56mm'}
        
        conn = cups.Connection()
        printers = conn.getPrinters()
        for printer in printers:
            conn.printFile(printer, filename, "PhotoBox", setting)
        

    def overlay_images(self, e) -> str:
        background = Image.open(self.path_img)
        scaled_background = background.resize(
            (
                int(int(self.setting_template["Width"]) / 3),
                int(int(self.setting_template["Height"]) / 3),
            )
        )
        buffered = BytesIO()
        scaled_background.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        self.row_preset.src_base64 = base64_image
        self.page.update()

    def back(self, e):
        self.page.scroll = "None"
        self.master.back_settings_template_cut_all()
