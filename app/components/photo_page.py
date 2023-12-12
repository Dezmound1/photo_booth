import flet as ft
import cv2
from PIL import Image

import time
import subprocess
import os
from io import BytesIO
import base64
import threading
import json

from components.buttons import MainButton, BackButton
from components.print_page import PrintPage


class PhotoPage:
    def __init__(self, page: ft.Page, master, name):
        self.master = master
        self.page = page
        self.name_template = name
        
        self.master.rerun_process_camera()
        
        self.name_category = self.master.session[4]
        self.setting_template = json.load(open(f"./templates/{self.name_category}/{self.name_template}.json"))
        self.replace = None
        self.size_y = self.setting_template["Photos"][0]["x"]
        self.size_x = self.setting_template["Photos"][0]["y"]

        self.timer_event = threading.Event()
        self.timer_text = ft.Row(
            controls=[
                ft.Text(
                    value="",
                    color="white",
                    size=60,
                    weight="bold",
                    opacity=0.5,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        self.limit_img = len([i["shoot"] for i in self.setting_template["Photos"]])

        if self.limit_img != max([i["shoot"] for i in self.setting_template["Photos"]]):
            self.limit_img = max([i["shoot"] for i in self.setting_template["Photos"]])
            self.replace = len([i["shoot"] for i in self.setting_template["Photos"]]) / max(
                [i["shoot"] for i in self.setting_template["Photos"]]
            )

        self.dir_photo = self.master.session[3]

        self.count = 1
        self.list_img = []

        self.quantity_image = self.count_files_in_folder(f"{self.dir_photo}/photo")

        self.button = MainButton("Сфотать", self.on_take_picture_button_click)
        self.canvas = ft.Image(
            src_base64="",
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        self.colum = ft.Column(
            controls=[
                ft.Text(
                    value="Вы прекрасны!",
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
                    ft.Column(
                        [
                            self.colum,
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Stack([self.canvas, self.timer_text]),
                            ft.Row(
                                [
                                    self.button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Column(controls=[BackButton("Назад", lambda e: self.back(e, self.name_category))]),
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        )

        self.cap = None
        self.connect_camera(3)

        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def update_loop(self):
        overlay_info = self.setting_template["Photos"][0]
        target_aspect_ratio = overlay_info["w"] / overlay_info["h"]

        # Предполагаем, что размер экрана доступен как self.screen_width и self.screen_height
        max_height = 550  # Изображение не должно превышать половину высоты экрана

        while True:
            if self.cap:
                ret, frame = self.cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)

                    current_aspect_ratio = img.width / img.height
                    if current_aspect_ratio > target_aspect_ratio:
                        new_width = int(img.height * target_aspect_ratio)
                        left = (img.width - new_width) // 2
                        right = left + new_width
                        img = img.crop((left, 0, right, img.height))
                    elif current_aspect_ratio < target_aspect_ratio:
                        new_height = int(img.width / target_aspect_ratio)
                        top = (img.height - new_height) // 2
                        bottom = top + new_height
                        img = img.crop((0, top, img.width, bottom))

                    # Дополнительно изменяем размер до целевых параметров
                    if max_height < overlay_info["h"]:
                        img = img.resize((overlay_info["w"] // 2, overlay_info["h"] // 2), Image.Resampling.LANCZOS)
                    else:
                        img = img.resize((overlay_info["w"], overlay_info["h"]), Image.Resampling.LANCZOS)

                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

                    self.canvas.src_base64 = img_str
                    self.page.update()
            time.sleep(0.05)

    def connect_camera(self, camera_num):
        timeout = 10  # время ожидания подключения в секундах
        start_time = time.time()
        while True:
            self.cap = cv2.VideoCapture(camera_num)
            if self.cap.isOpened():
                break
            elif (time.time() - start_time) > timeout:
                self.master.kill_process_camera()
                raise RuntimeError("Не удалось подключиться к камере")
            else:
                time.sleep(0.5)

    def take_picture(self, e):
        
        self.master.kill_process_camera()
        
        os.system(
            f'gphoto2 --capture-image-and-download --filename="{self.dir_photo}/photo/{self.quantity_image}.png"'
        )

        self.page.splash = None
        self.button.disabled = False
        self.page.update()

        self.master.rerun_process_camera()
        
        self.quantity_image += 1
        name_image = self.quantity_image - 1
        count = self.count
        self.list_img.append(name_image)
        overlay_info = self.setting_template["Photos"][0]
        x, y, w, h = overlay_info["x"], overlay_info["y"], overlay_info["w"], overlay_info["h"]

        # Путь к только что сделанному снимку
        photo_path = f"{self.dir_photo}/photo/{name_image}.png"

        # Открываем изображение и получаем его размеры
        overlay = Image.open(photo_path)
        target_aspect_ratio = w / h  # Целевое соотношение сторон

        # Получаем текущее соотношение сторон изображения
        current_aspect_ratio = overlay.width / overlay.height

        if current_aspect_ratio > target_aspect_ratio:
            # Если изображение слишком широкое, обрезаем по ширине
            new_width = int(overlay.height * target_aspect_ratio)
            left = (overlay.width - new_width) // 2
            right = (overlay.width + new_width) // 2
            top = 0
            bottom = overlay.height
            overlay = overlay.crop((left, top, right, bottom))
        elif current_aspect_ratio < target_aspect_ratio:
            # Если изображение слишком высокое, обрезаем по высоте
            new_height = int(overlay.width / target_aspect_ratio)
            top = (overlay.height - new_height) // 2
            bottom = (overlay.height + new_height) // 2
            left = 0
            right = overlay.width
            overlay = overlay.crop((left, top, right, bottom))

        # Изменение размера обрезанного изображения
        overlay = overlay.resize(
            (w, h), Image.Resampling.LANCZOS
        )  # Image.ANTIALIAS заменено на Image.Resampling.LANCZOS

        buffered = BytesIO()
        overlay.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

        if len(self.list_img) < self.limit_img:
            self.colum.controls.append(
                ft.Container(
                    ft.Stack(
                        [
                            ft.Image(src_base64=img_str),
                            ft.Container(
                                margin=10,
                                right=0,
                                border_radius=5,
                                width=60,
                                height=60,
                                content=ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="pink600",
                                    icon_size=40,
                                    tooltip="Удалить фотографию",
                                    on_click=lambda x: self.del_img(x, name_image, count),
                                ),
                            ),
                        ]
                    ),
                    border_radius=8,
                    padding=5,
                    width=350,
                    height=250,
                )
            )
            self.count += 1
            self.page.update()
        else:
            self.count += 1
            self.colum.controls.append(
                ft.Container(
                    ft.Stack(
                        [
                            ft.Image(src_base64=img_str),
                            ft.Container(
                                margin=10,
                                right=0,
                                border_radius=5,
                                width=60,
                                height=60,
                                content=ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="pink600",
                                    icon_size=40,
                                    tooltip="Удалить фотографию",
                                    on_click=lambda x: self.del_img(x, name_image, count),
                                ),
                            ),
                        ]
                    ),
                    border_radius=8,
                    padding=5,
                    width=350,
                    height=250,
                )
            )
            self.button.visible = False
            self.page.controls[0].controls[1].controls[1].controls[0] = MainButton(
                "Мне нравиться !", on_click=self.to_print
            )
            self.page.update()

    def del_img(self, e, name, count):
        self.colum.controls[count].visible = False
        self.page.controls[0].controls[1].controls[1].controls[0] = MainButton(
            "Сфотать", self.on_take_picture_button_click
        )
        try:
            self.list_img.remove(name)
        except:
            pass
        os.system(f"rm {self.dir_photo}/photo/{name}.png")
        self.page.update()

    def count_files_in_folder(self, folder_path):
        try:
            files = [int(name.split(".")[0]) for name in os.listdir(folder_path)]
            return sorted(files)[-1] + 1
        except Exception as e:
            return 0

    def back(self, e, name):
        self.master.user_choise()

    def to_print(self, e):
        self.page.splash = ft.ProgressBar()
        self.button.disabled = True
        self.page.update()
        path_img = self.overlay_images()
        self.page.splash = None
        self.button.disabled = False
        self.page.update()
        self.master.new_win(PrintPage, (path_img, False))

    def overlay_images(self) -> str:
        if self.replace is not None:
            self.list_img = self.list_img * int(self.replace)

        # Путь к фоновому изображению из настроек шаблона
        background_path = f"./templates/{self.name_category}/{self.name_template}.png"
        background = Image.open(background_path)

        for overlay_info, name_img in zip(self.setting_template["Photos"], self.list_img):
            shoot = name_img
            x, y, w, h = overlay_info["x"], overlay_info["y"], overlay_info["w"], overlay_info["h"]

            # Загрузка изображения для наложения
            overlay_path = f"{self.dir_photo}/photo/{shoot}.png"
            overlay = Image.open(overlay_path)

            # Обрезка и изменение размера изображения для наложения
            aspect_ratio = w / h
            overlay_aspect_ratio = overlay.width / overlay.height

            if overlay_aspect_ratio > aspect_ratio:
                # Широкое изображение
                new_width = int(overlay.height * aspect_ratio)
                overlay = overlay.crop(
                    ((overlay.width - new_width) // 2, 0, (overlay.width + new_width) // 2, overlay.height)
                )
            elif overlay_aspect_ratio < aspect_ratio:
                # Высокое изображение
                new_height = int(overlay.width / aspect_ratio)
                overlay = overlay.crop(
                    (0, (overlay.height - new_height) // 2, overlay.width, (overlay.height + new_height) // 2)
                )

            # Изменение размера обрезанного изображения
            overlay = overlay.resize((w, h), Image.Resampling.LANCZOS)

            # Установка прозрачности для изображения, если оно не имеет альфа-канала
            if overlay.mode != "RGBA":
                overlay = overlay.convert("RGBA")

            # Наложение изображения на фон
            background.paste(overlay, (x, y), overlay)

        # Сохранение итогового изображения
        output_template = f"{self.dir_photo}/photo_templates/{self.name_template}_{self.count_files_in_folder(f'{self.dir_photo}/photo_templates')}.png"
        background.save(output_template, format="PNG")
        return output_template

    def start_timer(self, remaining_time):
        if remaining_time > 0:
            self.timer_text.controls[0].value = str(remaining_time)
            self.page.update()
            threading.Timer(1, self.start_timer, args=[remaining_time - 1]).start()
        else:
            self.timer_text.controls[0].value = str("")
            self.timer_event.set()

    def on_take_picture_button_click(self, e):
        self.timer_event.clear()
        self.page.splash = ft.ProgressBar()
        self.button.disabled = True
        self.page.update()
        self.start_timer(3)
        self.timer_event.wait()
        self.take_picture(None)
