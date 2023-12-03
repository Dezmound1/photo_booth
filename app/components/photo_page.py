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

from components.buttons import MainButton
from components.print_page import PrintPage


class PhotoPage:
    def __init__(self, page: ft.Page, master, name):
        self.master = master
        self.page = page
        self.name_template = name
        self.name_category = self.master.session[4]
        self.setting_template = json.load(open(f"./templates/{self.name_category}/{self.name_template}.json"))
        self.replace = None
        
        self.limit_img = len([i["shoot"] for i in self.setting_template["Photos"]])
        
        if self.limit_img != max([i["shoot"] for i in self.setting_template["Photos"]]):
            self.limit_img = max([i["shoot"] for i in self.setting_template["Photos"]])
            self.replace = len([i["shoot"] for i in self.setting_template["Photos"]])/max([i["shoot"] for i in self.setting_template["Photos"]])
            
        self.dir_photo = self.master.session[3]
        
        
        self.count = 1
        self.list_img = []

        self.command = "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video3"
        self.pro = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        self.quantity_image = self.count_files_in_folder(f"{self.dir_photo}/photo")

        self.button = MainButton("Создать", self.take_picture)
        self.canvas = ft.Image(
            src_base64="",
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
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
                    ft.Column(
                        [
                            self.colum,
                        ]
                    ),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    self.canvas,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(
                                [
                                    self.button,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    ft.Column(
                        [
                            ft.Column(controls=[MainButton("Назад", lambda e: self.back(e, self.name_category))]),
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
        while True:
            if self.cap:
                ret, frame = self.cap.read()
                corner = int(1)
                corner_crop = 1 + abs(corner) * 0.015
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    (h, w) = frame.shape[:2]
                    center = (int(w / 2), int(h / 2))
                    rotation_matrix = cv2.getRotationMatrix2D(center, corner, corner_crop)
                    rotated = cv2.warpAffine(frame, rotation_matrix, (w, h))
                    new_frame = cv2.resize(rotated, (w, h))
                    img = Image.fromarray(new_frame)
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
                if self.pro:
                    self.pro.kill()
                os.system("pkill ffmpeg")
                raise RuntimeError("Не удалось подключиться к камере")
            else:
                time.sleep(0.5)

    def take_picture(self, e):
        self.page.splash = ft.ProgressBar()
        self.button.disabled = True
        self.page.update()
        

        if self.pro:
            self.pro.kill()

        os.system("pkill ffmpeg")
        os.system(f"""gphoto2 --capture-image-and-download --filename="{self.dir_photo}/photo/{self.quantity_image}.png" """)

        self.page.splash = None
        self.button.disabled = False
        self.page.update()

        self.pro = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.quantity_image += 1
        name_image = self.quantity_image - 1
        count = self.count
        self.list_img.append(name_image)

        if len(self.list_img) < self.limit_img:
            self.colum.controls.append(
                ft.Container(
                    ft.Stack(
                        [
                            ft.Image(src=f"{self.dir_photo}/photo/{name_image}.png"),
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
                                    on_click=lambda x : self.del_img(x,name_image, count),
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
            self.colum.controls.append(
                ft.Container(
                    ft.Stack(
                        [
                            ft.Image(src=f"{self.dir_photo}/photo/{name_image}.png"),
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
                                    on_click=lambda x : self.del_img(x,name_image, count),
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
            self.page.controls[0].controls[1].controls[1].controls[0] = MainButton("Сформировать", on_click=self.to_print)
            self.page.update()
            
    def del_img(self, e, name, count):
        self.colum.controls[count].visible = False
        self.list_img.remove(name)
        os.system(f"rm {self.dir_photo}/photo/{name}.png")

    def count_files_in_folder(self, folder_path):
        try:
            files = [int(name.split(".")[0]) for name in os.listdir(folder_path)]
            return sorted(files)[-1]+1
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
        
    def overlay_images(self)->str:
        if self.replace is not None:
            self.list_img = self.list_img*int(self.replace)
        
        background = Image.open(f"./templates/{self.name_category}/{self.name_template}.png")
        
        for overlay_info, name_img in zip(self.setting_template["Photos"], self.list_img):
            shoot = name_img
            x = overlay_info["x"]
            y = overlay_info["y"]
            w = overlay_info["w"]
            h = overlay_info["h"]

            overlay = Image.open(f"{self.dir_photo}/photo/{shoot}.png")

            overlay = overlay.resize((w, h))

            if overlay.mode != 'RGBA':
                overlay = overlay.convert('RGBA')

            background.paste(overlay, (x, y), overlay)

        name = self.count_files_in_folder(f"{self.dir_photo}/photo_templates")
        output_path = f"{self.dir_photo}/photo_templates/{name}.png"
        background.save(output_path, format='PNG')
        return output_path
