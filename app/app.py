import flet as ft
import sqlite3
import cups
import cv2

import time
import threading
import subprocess
import os

from components.main import Main
from components.user_choise import UserChoise
from components.history import HistoryPage
from components.photo_history import PhotoHistory
from components.settings_page import Settings
from components.settings.test_templates import TemplateTest
from components.settings.test_cut_template import TemplateCutTest
from components.page_preview import PreviewsPage


class Pages:
    def __init__(self, page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.views = None
        self.conn = sqlite3.connect("./base.db", check_same_thread=False)
        self.cur = self.conn.cursor()

        self.command = "gphoto2 --stdout --capture-movie | ffmpeg -i - -vcodec rawvideo -pix_fmt yuv420p -threads 0 -f v4l2 /dev/video3"
        self.process_camera = None
        self.rerun_process_camera()

        self.cap = None
        self.connect_camera(3)
        
        self.page.window_full_screen = True

        self.session = None
        page.banner = ft.Container(
            border_radius=40,
            width=70,
            height=70,
            bgcolor=ft.colors.RED,
            opacity=0.5,
            alignment=ft.alignment.center,
        )

        thread = threading.Thread(target=self.check_jobs)
        thread.daemon = True
        thread.start()

        self.new_win(Main)

    def connect_camera(self, camera_num):
        timeout = 10
        start_time = time.time()
        while True:
            self.cap = cv2.VideoCapture(camera_num)
            if self.cap.isOpened():
                break
            elif (time.time() - start_time) > timeout:
                self.kill_process_camera()
                break
            else:
                time.sleep(0.5)

    def get_total_active_jobs(self):
        conn = cups.Connection()

        total_jobs = 0

        for task in conn.getJobs().keys():
            task_to_id = conn.getJobAttributes(task)
            total_jobs += int(task_to_id["copies"])

        return total_jobs

    def new_win(self, class_name_page, params=None):
        self.kill_process_camera()
        if self.views:
            if not params:
                self.page.clean()
                self.views = class_name_page(self.page, self)
            else:
                self.page.clean()
                self.views = class_name_page(self.page, self, params)
        else:
            if not params:
                self.page.clean()
                self.views = class_name_page(self.page, self)
            else:
                self.page.clean()
                self.views = class_name_page(self.page, self, params)

    def back_main_page(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = Main(self.page, self)

    def user_choise(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = UserChoise(self.page, self)

    def back_settings(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = HistoryPage(self.page, self)

    def back_settings_template(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = Settings(self.page, self)

    def back_settings_template_all(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = TemplateTest(self.page, self)
    
    def back_settings_template_cut_all(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = TemplateCutTest(self.page, self)

    def back_photo_history(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = PhotoHistory(self.page, self)

    def close_banner(self, e):
        self.kill_process_camera()
        self.page.banner.visible = False
        self.page.update()

    def show_banner_click(self, e):
        self.kill_process_camera()
        self.page.banner.visible = True
        self.page.update()

    def check_jobs(self):
        while True:
            total_jobs = self.get_total_active_jobs()
            if total_jobs > 0:
                self.page.banner.visible = True
                self.page.banner.content = ft.Text(
                    f"{total_jobs}",
                    color="white",
                    size=40,
                    weight="bold",
                    text_align="center",
                )
                self.page.update()
            else:
                self.page.banner.visible = False
                self.page.banner.content = ft.Text(
                    f"{total_jobs}",
                    color="white",
                    size=40,
                    weight="bold",
                    text_align="center",
                )
                self.page.update()
            time.sleep(1)

    def go_camera_main(self):
        self.kill_process_camera()
        self.page.clean()
        self.views = PreviewsPage(self.page, self)

    def kill_process_camera(
        self,
    ):
        if self.process_camera is None:
            pass
        else:
            self.process_camera.terminate()

            if self.process_camera.poll() is None:
                self.process_camera.kill()

            os.system("pkill ffmpeg")

    def rerun_process_camera(
        self,
    ):
        self.process_camera = subprocess.Popen(
            self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )


def main(page: ft.Page):
    os.system("./add_usb_printers.sh")
    Pages(page=page)


if __name__ == "__main__":
    ft.app(target=main)
