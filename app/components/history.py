import flet as ft
import shutil
import psutil

import os

from components.buttons import MainButton, MainText, RedButton
from components.photo_history import PhotoHistory


class HistoryPage:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.master.cur.execute("SELECT * FROM session")
        self.list_session = self.master.cur.fetchall()
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Hello, world!"),
            action="Alright!",
        )

        self.title = ft.Text("История сессий", size=30)
        self.session_comment = MainText("Краткое описание")

        self.button_back = RedButton("Назад", self.back_main)

        self.lv = ft.ListView(expand=1)

        self.page.add(ft.Container(content=self.button_back, alignment=ft.alignment.top_left))
        self.page.add(
            ft.Row(
                [self.title],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.add(self.lv)
        for i in self.list_session:
            self.creat_row(i)
            self.page.update()

    def creat_row(self, session):
        self.lv.controls.append(
            ft.Column(
                [
                    ft.Row(
                        [
                            MainText(str(session[0])),
                            MainText(session[3].split("/")[-1]),
                            MainText(session[4]),
                            MainButton("Сохранить", lambda e: self.copy_to_all_usb_drives(e, session[0])),
                            MainButton("Продолжить", lambda e: self.resume_session(e, session[0])),
                            MainButton("Фотографии", lambda e: self.photo_session(e, session[0])),
                            MainButton("Удалить", lambda e: self.del_session(e, session[0])),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                ]
            )
        )

    def back_main(self, e):
        self.master.back_main_page()

    def del_session(self, e, session_id):
        self.master.cur.execute("DELETE FROM session WHERE id = ?", (session_id,))
        self.master.conn.commit()
        self.master.new_win(HistoryPage)

    def photo_session(self, e, session_id):
        self.master.cur.execute("SELECT * FROM session WHERE id = ?", (session_id,))
        self.master.session = self.master.cur.fetchone()
        self.master.new_win(PhotoHistory)

    def resume_session(self, e, session_id):
        self.master.cur.execute("SELECT * FROM session WHERE id = ?", (session_id,))
        self.master.session = self.master.cur.fetchone()
        self.master.user_choise()

    def copy_to_all_usb_drives(self, e, session_id):
        self.master.cur.execute("SELECT * FROM session WHERE id = ?", (session_id,))
        sesion = self.master.cur.fetchone()
        source_directory, name_dir = sesion[3], sesion[3].split("/")[-1]

        usb_drives = [
            (partition.device, partition.mountpoint)
            for partition in psutil.disk_partitions()
            if partition.fstype == "vfat" and partition.device.startswith("/dev/sdb")
        ]

        if not usb_drives:
            print("Нет подключенных флеш-накопителей.")
            return

        # Копирование на каждый флеш-накопитель
        for usb_drive, mount_point in usb_drives:
            target_directory = os.path.join(mount_point, name_dir)

            try:
                # Проверка существования папки и создание уникального имени при необходимости
                counter = 1
                while os.path.exists(target_directory):
                    target_directory = os.path.join(mount_point, f"{name_dir}_{counter}")
                    counter += 1

                # Копирование содержимого исходной папки на флеш-накопитель
                shutil.copytree(source_directory, target_directory)

                self.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Содержимое скопировано на {usb_drive} в {target_directory}")
                )
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as e:
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка при копировании на {usb_drive}: {e}"))
                self.page.snack_bar.open = True
                self.page.update()
