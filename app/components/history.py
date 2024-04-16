import flet as ft
import shutil
import psutil

import os
from time import sleep

from components.buttons import MainButton, MainText, BackButton, RedButton
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

        self.button_back = RedButton("Назад", on_click=self.back_main)

        self.lv = ft.Column(scroll=ft.ScrollMode.ALWAYS, height=500)
        content = ft.Column(
            controls=[
                self.button_back,
                ft.Row(
                    [self.title],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                self.lv,
            ]
        )
        self.page.add(
            ft.Container(
                image_src="./img/bg.png",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                content=content,
                alignment=ft.alignment.center,
            )
        )
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
                            ft.Text(str(session[-1]), size=20),
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
                                bgcolor=ft.colors.with_opacity(1, "#FF544D"),
                                style=ft.ButtonStyle(
                                    side={
                                        ft.MaterialState.DEFAULT: ft.BorderSide(
                                            1,
                                            ft.colors.with_opacity(
                                                1, "#FF544D"
                                            ),
                                        ),
                                    },
                                    shape={
                                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                            radius=20
                                        ),
                                    },
                                ),
                                color=ft.colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                text="Продолжить",
                                on_click=lambda e: self.resume_session(
                                    e, session[0]
                                ),
                                height=40,
                                width=150,
                                bgcolor=ft.colors.with_opacity(1, "#FF544D"),
                                style=ft.ButtonStyle(
                                    side={
                                        ft.MaterialState.DEFAULT: ft.BorderSide(
                                            1,
                                            ft.colors.with_opacity(
                                                1, "#FF544D"
                                            ),
                                        ),
                                    },
                                    shape={
                                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                            radius=20
                                        ),
                                    },
                                ),
                                color=ft.colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                text="Фотографии",
                                on_click=lambda e: self.photo_session(
                                    e, session[0]
                                ),
                                height=40,
                                width=150,
                                bgcolor=ft.colors.with_opacity(1, "#FF544D"),
                                style=ft.ButtonStyle(
                                    side={
                                        ft.MaterialState.DEFAULT: ft.BorderSide(
                                            1,
                                            ft.colors.with_opacity(
                                                1, "#FF544D"
                                            ),
                                        ),
                                    },
                                    shape={
                                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                            radius=20
                                        ),
                                    },
                                ),
                                color=ft.colors.WHITE,
                            ),
                            ft.ElevatedButton(
                                text="Удалить",
                                on_click=lambda e: self.alert(e, session[0]),
                                height=40,
                                width=150,
                                bgcolor=ft.colors.with_opacity(1, "#FF544D"),
                                style=ft.ButtonStyle(
                                    side={
                                        ft.MaterialState.DEFAULT: ft.BorderSide(
                                            1,
                                            ft.colors.with_opacity(
                                                1, "#FF544D"
                                            ),
                                        ),
                                    },
                                    shape={
                                        ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(
                                            radius=20
                                        ),
                                    },
                                ),
                                color=ft.colors.WHITE,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            )
        )

    def alert(self, e, session_id):
        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=MainText("Подтвердите"),
            content=MainText("Хотите удалить сессию?"),
            actions=[
                MainButton(
                    "Да", on_click=lambda e: self.del_session(e, session_id)
                ),
                RedButton("Нет", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

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
        self.dlg_modal.open = False
        self.page.update()
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
        self.page.dialog.open = False
        self.page.update()

    def get_unique_target_directory(self, mount_point, name_dir):
        target_directory = os.path.join(mount_point, name_dir)
        counter = 1
        while os.path.exists(target_directory):
            target_directory = os.path.join(
                mount_point, f"{name_dir}_{counter}"
            )
            counter += 1
        return target_directory

    def show_banner(self, message):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text(message), on_dismiss=self.close_banner
        )
        self.page.dialog.open = True
        self.page.update()

    def update_banner(self, message):
        if self.page.dialog:
            self.page.dialog.title = ft.Text(message)
            self.page.update()

    def copy_to_all_usb_drives(self, e, session_id):
        self.master.cur.execute(
            "SELECT * FROM session WHERE id = ?", (session_id,)
        )
        session = self.master.cur.fetchone()
        source_directory = session[3] + "/photo_templates"
        total_files = sum(
            [len(files) for r, d, files in os.walk(source_directory)]
        )

        usb_drives = [
            (partition.device, partition.mountpoint)
            for partition in psutil.disk_partitions()
            if partition.fstype == "vfat"
        ]

        if not usb_drives:
            self.show_banner("Нет подключенных флеш-накопителей.")
            return

        for usb_drive, mount_point in usb_drives:
            try:
                target_directory = self.get_unique_target_directory(
                    mount_point, session[3].split("/")[-1]
                )
                copied_files = 0
                self.show_banner("Началось копирование")
                for root, dirs, files in os.walk(source_directory):
                    for file in files:
                        source_file = os.path.join(root, file)
                        relative_path = os.path.relpath(
                            source_file, source_directory
                        )
                        destination_file = os.path.join(
                            target_directory, relative_path
                        )
                        os.makedirs(
                            os.path.dirname(destination_file), exist_ok=True
                        )
                        shutil.copy2(source_file, destination_file)
                        copied_files += 1
                        percent = (copied_files / total_files) * 100
                        self.update_banner(
                            f"Копирование: {percent:.2f}% завершено на {usb_drive}"
                        )
                self.show_banner(
                    f"Содержимое скопировано на {usb_drive} в {target_directory}"
                )
            except Exception as ex:
                pass
