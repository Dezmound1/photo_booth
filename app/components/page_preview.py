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

        self.master.rerun_process_camera()

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

        self.update_thread = threading.Thread(target=self.update_loop)
        self.update_thread.daemon = True
        self.update_thread.start()

    def update_loop(self):
        while True:
            if self.master.cap:
                ret, frame = self.master.cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    img = Image.fromarray(frame)

                    buffered = BytesIO()
                    img.save(buffered, format="JPEG")
                    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    self.canvas.src_base64 = img_str
                    self.page.update()
            time.sleep(0.05)

    def go_photo(self, e):
        self.master.user_choise()
