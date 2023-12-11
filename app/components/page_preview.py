import flet as ft
import cv2
from PIL import Image

import time
import os
from io import BytesIO
import base64
import threading
import subprocess

from components.buttons import MainButton


class PreviewsPage:
    def __init__(self, page: ft.Page, master):
        self.master = master
        self.page = page

        self.command = "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video3"
        self.pro = subprocess.Popen(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.button = MainButton("Сфотать", self.go_photo)
        self.canvas = ft.Image(
            src_base64="",
            fit=ft.ImageFit.NONE,
            repeat=ft.ImageRepeat.NO_REPEAT,
            border_radius=ft.border_radius.all(10),
        )
        self.page.add(
            ft.Row(
                [
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
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
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
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)

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
                
    def go_photo(self, e):
        self.master.user_choise()