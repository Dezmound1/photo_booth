import flet as ft
from PIL import Image

from components.buttons import RedButton
from components.photo_page import PhotoPage

import os
import time
import threading
import json
import base64
from io import BytesIO


class UserChoise:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.name_category = self.master.session[4]
        self.stop_thread = False
        self.last_activity_time = time.time()
        self.inactivity_timeout = 240

        self.index = 1
        self.list_template = [
            name.split(".")[0]
            for name in os.listdir(f"./templates/{self.name_category}")
            if name.split(".")[1] == "png"
        ]
        self.count_open = 1
        self.page.add(
            ft.Column(controls=[RedButton("Назад", lambda e: self.back(e))]),
        )
        self.cards = ft.Row(expand=1, width=1600, scroll="AUTO")
        self.content = ft.Row(
            [
                ft.Row([self.cards], width=1600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.buttom_event = ft.Row(
            [
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_DOUBLE_ARROW_LEFT, on_click=self.mun_2),
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_ARROW_LEFT, on_click=self.mun_1),
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_ARROW_RIGHT, on_click=self.add_1),
                ft.IconButton(icon_size=60, icon=ft.icons.KEYBOARD_DOUBLE_ARROW_RIGHT, on_click=self.add_2),
            ],
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
        )
        self.page.add(
            ft.Row(
                [
                    ft.Text(
                        "Выберите шаблон",
                        style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.add(self.content)

        for i in self.list_template:
            self.creact_container(i)
            self.page.update()

        self.page.add(self.buttom_event)

        self.mutex = threading.Lock()

        # Создаем поток отслеживания неактивности
        self.inactivity_thread = threading.Thread(target=self.track_inactivity)
        self.inactivity_thread.daemon = True
        self.inactivity_thread.start()
        self.page.update()

    def add_1(self, e):
        if self.count_open + 1 < self.index:
            self.count_open += 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)
        self.reset_timer()

    def add_2(self, e):
        if self.count_open + 2 < self.index:
            self.count_open += 2
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

        elif self.count_open + 1 < self.index:
            self.count_open += 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)
        self.reset_timer()

    def mun_1(self, e):
        if self.count_open - 1 > 0:
            self.count_open -= 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)
        self.reset_timer()

    def mun_2(self, e):
        if self.count_open - 2 > 0:
            self.count_open -= 2
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

        elif self.count_open - 1 > 0:
            self.count_open -= 1
            self.cards.scroll_to(key=f"{self.count_open}", duration=10)

        self.reset_timer()

    def creact_container(self, name):
        i = self.index
        self.cards.controls.append(
            ft.ElevatedButton(
                content=ft.Image(
                    src_base64 = self.overlay_images(1,name),
                    width=320,
                    height=622,
                ),
                key=str(i),
                on_click=lambda e: self.photo_maker(e, name),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                ),
            )
        )

        self.index += 1

    def photo_maker(self, e, name):
        self.stop_tracking_thread()
        self.master.new_win(PhotoPage, name)

    def back(self, e):
        self.stop_tracking_thread()
        self.master.go_camera_main()

    def reset_timer(self):
        with self.mutex:
            self.last_activity_time = time.time()

    def track_inactivity(self):
        while not self.stop_thread:
            current_time = time.time()
            with self.mutex:
                if current_time - self.last_activity_time > self.inactivity_timeout:
                    self.back(None)  # Вызываем метод back, если прошло более 5 минут бездействия
            time.sleep(60)
            
    def stop_tracking_thread(self):
        self.stop_thread = True
        
        
    def overlay_images(self,e,img_name):

        background = Image.open(f"./templates/{self.name_category}/{img_name}.png")
        setting_template = json.load(open(f"./templates/{self.name_category}/{img_name}.json"))
        list_img = ["./templates/test_img/0.png"] * len(setting_template["Photos"])

        for overlay_info, name_img in zip(setting_template["Photos"], list_img):
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
            (int(int(setting_template["Width"]) / 2), int(int(setting_template["Height"]) / 2))
        )

        buffered = BytesIO()
        scaled_background.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        return base64_image
