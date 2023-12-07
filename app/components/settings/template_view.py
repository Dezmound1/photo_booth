import flet as ft
from PIL import Image

import json
import base64
from io import BytesIO

from components.buttons import RedButton
from components.buttons import MainButton


class TemplateView:
    def __init__(self, page, master, path_img):
        self.page = page
        self.master = master
        self.path_img = path_img
        self.settings_path = self.path_img.replace(".png", ".json")
        with open(self.settings_path, "r") as file:
            self.setting_template = json.load(file)

        self.replace = None
        self.back_btn = RedButton("Назад", self.back)
        self.page.add(self.back_btn)

        self.limit_img = len([i["shoot"] for i in self.setting_template["Photos"]])

        if self.limit_img != max([i["shoot"] for i in self.setting_template["Photos"]]):
            self.limit_img = max([i["shoot"] for i in self.setting_template["Photos"]])
            self.replace = len([i["shoot"] for i in self.setting_template["Photos"]]) / max(
                [i["shoot"] for i in self.setting_template["Photos"]]
            )

        self.list_img = ["./templates/test_img/0.png"] * self.limit_img

        self.row_preset = ft.Image(
            src_base64="",
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        self.overlay_images(1)
        
        self.settings = ft.GridView(
            expand=1,
            runs_count=4,
        )

        self.settings.controls = [self.creact_setting(i) for i in range(len(self.setting_template["Photos"]))]
        self.settings.controls.append(
            ft.Row(
                [
                    MainButton("Просмотреть", self.overlay_images)  
                ]
            )
        )
        self.settings.controls.append(
            ft.Row(
                [
                    MainButton("Сохранить", self.save_setting)  
                ]
            )
        )
        
        
        self.page.add(ft.Row([self.row_preset, self.settings]))
        self.page.update()
    
    def save_setting(self,e):
        with open(self.settings_path, 'w') as json_file:
            # Используете метод dump для записи данных в файл
            json.dump(self.setting_template, json_file)
        
        self.back(1)
        

    def creact_setting(self, i):
        return ft.Row(
            [
                ft.Text(f"Фото {i}", size=30),
                ft.Column(
                    [
                        ft.IconButton(ft.icons.ARROW_DROP_UP, on_click=lambda e: self.plus_click(e, 1, i)),
                        ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100),
                        ft.IconButton(ft.icons.ARROW_DROP_DOWN, on_click=lambda e: self.minus_click(e, 1, i)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column(
                    [
                        ft.IconButton(ft.icons.ARROW_RIGHT, on_click=lambda e: self.plus_click(e, 2, i)),
                        ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100),
                        ft.IconButton(ft.icons.ARROW_LEFT, on_click=lambda e: self.minus_click(e, 2, i)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def minus_click(self, e, num, index):
        self.settings.controls[index].controls[num].controls[1].value = str(
            int(self.settings.controls[index].controls[num].controls[1].value) - 1
        )
        if num == 1:
            self.setting_template["Photos"][index]["y"] += 1
        else:
            self.setting_template["Photos"][index]["x"] -= 1
            
        self.setting_template["Photos"][index]
        self.page.update()

    def plus_click(self, e, num, index):
        self.settings.controls[index].controls[num].controls[1].value = str(
            int(self.settings.controls[index].controls[num].controls[1].value) + 1
        )
        if num == 1:
            self.setting_template["Photos"][index]["y"] -= 1
        else:
            self.setting_template["Photos"][index]["x"] += 1
            
        self.page.update()

    def overlay_images(self,e) -> str:
        self.page.splash = ft.ProgressBar()
        self.page.update()
        if self.replace is not None:
            self.list_img = self.list_img * int(self.replace)

        background = Image.open(self.path_img)

        for overlay_info, name_img in zip(self.setting_template["Photos"], self.list_img):
            shoot = name_img
            x = overlay_info["x"]
            y = overlay_info["y"]
            w = overlay_info["w"]
            h = overlay_info["h"]

            overlay = Image.open(shoot)

            overlay = overlay.resize((w, h))

            if overlay.mode != "RGBA":
                overlay = overlay.convert("RGBA")

            background.paste(overlay, (x, y), overlay)

        scaled_background = background.resize(
            (int(int(self.setting_template["Width"]) / 2), int(int(self.setting_template["Height"]) / 2))
        )

        buffered = BytesIO()
        scaled_background.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        self.row_preset.src_base64 = base64_image
        self.page.splash = None
        self.page.update()

    def back(self, e):
        self.master.back_settings_template_all()
