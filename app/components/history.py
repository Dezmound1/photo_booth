import flet as ft
import shutil
import psutil

import os

from components.buttons import MainButton, MainText, BackButton
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

        self.button_back = BackButton("Назад", on_click=self.back_main)

        self.lv = ft.Column(
            scroll=ft.ScrollMode.ALWAYS,
            height=500
        )
        

        self.page.add(self.button_back)
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
                            ft.Text(str(session[0]), size=20),
                            ft.Text(
                                str(session[3].split("/")[-1]),
                                width=200,
                                size=20,
                            ),
                            ft.Text(str(session[4]), size=20),
                            ft.ElevatedButton(
                                text="Сохранить",
                                on_click=lambda e: self.copy_to_all_usb_drives(
                                    e, session[0]
                                ),
                                height=40,
                                width=150,
                            ),
                            ft.ElevatedButton(
                                text="Продолжить",
                                on_click=lambda e: self.resume_session(
                                    e, session[0]
                                ),
                                height=40,
                                width=150,
                            ),
                            ft.ElevatedButton(
                                text="Фотографии",
                                on_click=lambda e: self.photo_session(
                                    e, session[0]
                                ),
                                height=40,
                                width=150,
                            ),
                            ft.ElevatedButton(
                                text="Удалить",
                                on_click=lambda e: self.del_session(
                                    e, session[0]
                                ),
                                height=40,
                                width=150,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            )
        )

    def back_main(self, e):
        self.page.scroll = "None"
        self.master.back_main_page()

    def del_session(self, e, session_id):
        self.master.cur.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        )
        path = self.master.cur.fetchone()[3]
        self.master.cur.execute(
            "DELETE FROM session WHERE id = ?", (session_id,)
        )
        os.system(f"rm -fr {path}")
        self.master.conn.commit()
        self.master.new_win(HistoryPage)

    def photo_session(self, e, session_id):
        self.master.cur.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        )
        self.master.session = self.master.cur.fetchone()
        self.master.new_win(PhotoHistory)

    def resume_session(self, e, session_id):
        self.master.cur.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        )
        self.master.session = self.master.cur.fetchone()
        self.master.go_camera_main()

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()


    def copy_to_all_usb_drives(self, e, session_id):
        self.master.cur.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        )
        sesion = self.master.cur.fetchone()
        source_directory, name_dir = sesion[3]+"/photo_templates", sesion[3].split("/")[-1]
        print(source_directory, name_dir)
        usb_drives = [
            (partition.device, partition.mountpoint)
            for partition in psutil.disk_partitions()
            if partition.fstype == "vfat"
        ]
        print(usb_drives)
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
                    target_directory = os.path.join(
                        mount_point, f"{name_dir}_{counter}"
                    )
                    counter += 1
                self.page.banner = ft.Banner(
                    bgcolor=ft.colors.AMBER_100,
                    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
                    content=ft.Text(
                        f"Cодержимое скопировано на {usb_drive} в {target_directory}"
                    ),
                    actions=[
                        ft.TextButton("Закрыть", on_click=self.close_banner),
                    ],
                )
                print(f"Cодержимое скопировано на {usb_drive} в {target_directory}")
                self.page.banner.open = True
                self.page.update()
                # Копирование содержимого исходной папки на флеш-накопитель
                shutil.copytree(source_directory, target_directory)
            except Exception as e:
                self.page.banner.open = False
                print(e)

