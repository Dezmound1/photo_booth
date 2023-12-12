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
                    src=self.overlay_images(1, name),
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

    def overlay_images(self, e, img_name):
        output_folder = f"./prive_template/{self.name_category}"
        output_path = f"{output_folder}/{img_name}.png"

        # Проверяем, существует ли уже обработанное изображение
        if os.path.exists(output_path):
            return output_path

        # Загружаем настройки шаблона
        setting_template_path = f"./templates/{self.name_category}/{img_name}.json"
        if not os.path.exists(setting_template_path):
            raise FileNotFoundError(f"Setting template file not found: {setting_template_path}")

        setting_template = json.load(open(setting_template_path))

        # Загружаем фоновое изображение
        template_path = f"./templates/{self.name_category}/{img_name}.png"
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")

        background = Image.open(template_path)

        # Предположим, что для демонстрации используется тестовое изображение
        test_image_path = "./templates/test_img/0.png"

        for overlay_info in setting_template["Photos"]:
            x, y, w, h = overlay_info["x"], overlay_info["y"], overlay_info["w"], overlay_info["h"]

            # Загружаем и обрабатываем изображение для наложения
            overlay = Image.open(test_image_path)
            target_aspect_ratio = w / h
            overlay = self.resize_and_crop(overlay, target_aspect_ratio, w, h)

            if overlay.mode != "RGBA":
                overlay = overlay.convert("RGBA")

            background.paste(overlay, (x, y), overlay)

        # Сохраняем обработанное изображение
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        background.save(output_path, format="PNG")

        return output_path

    def resize_and_crop(self, image, target_aspect_ratio, new_width, new_height):
    # Вычисляем соотношение сторон исходного изображения
        current_aspect_ratio = image.width / image.height

        # Определяем, нужно ли масштабировать по ширине или по высоте
        if current_aspect_ratio > target_aspect_ratio:
            # Масштабируем по высоте, обрезаем по ширине
            scaled_height = int(new_width / target_aspect_ratio)
            image = image.resize((new_width, scaled_height), Image.Resampling.LANCZOS)
        else:
            # Масштабируем по ширине, обрезаем по высоте
            scaled_width = int(new_height * target_aspect_ratio)
            image = image.resize((scaled_width, new_height), Image.Resampling.LANCZOS)

        # Вычисляем координаты для обрезки
        left = (image.width - new_width) // 2
        top = (image.height - new_height) // 2
        right = left + new_width
        bottom = top + new_height

        # Обрезаем изображение
        image = image.crop((left, top, right, bottom))
        return image

