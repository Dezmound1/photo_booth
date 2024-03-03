import flet as ft

import os
from datetime import datetime
import uuid

from components.buttons import RedButton, MainText
from components.const import PathEnum


class SessionList:
    def __init__(self, page, master, name):
        self.master = master
        self.page = page
        self.name = name

        self.namelist = os.listdir(PathEnum.mnt_path.value)
        try:
            self.namelist.remove("test_img")
        except:
            pass

        self.button_back = RedButton("Назад", self.back_main)

        self.row = ft.GridView(expand=True, runs_count=4)

        content = ft.Column(
            [
                ft.Row(
                    [self.button_back],
                    alignment=ft.MainAxisAlignment.START,
                    visible=True,
                ),
                self.row,
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        for i in self.namelist:
            self.row.controls.append(self.creat_buttom(i))

        self.page.add(
            ft.Container(
                image_src="./img/bg.png",
                image_fit=ft.ImageFit.COVER,
                expand=True,
                content=content,
                alignment=ft.alignment.center,
            )
        )

        self.page.update()

    def creat_buttom(self, name):
        return ft.Container(
            content=MainText(f"{name}"),
            margin=10,
            padding=10,
            alignment=ft.alignment.center,
            bgcolor=ft.colors.GREY_700,
            width=200,
            height=200,
            border_radius=10,
            on_click=lambda e: self.userlist(e, name),
        )

    def userlist(self, e, name):
        date = str(datetime.now().date())
        name_dir = "./photo_session/" + self.name + "_" + str(uuid.uuid1()).split("-")[-1] + "_" + date
        os.makedirs(name_dir)
        os.makedirs(name_dir + "/photo")
        os.makedirs(name_dir + "/photo_templates")
        os.makedirs(name_dir + "/photo_templates/dir_0")

        self.master.cur.execute(
            "INSERT INTO session (name, date, dir, topic, num_printed) VALUES (?, ?, ?, ?, ?)",
            (self.name, date, name_dir, name, 0),
        )
        last_row_id = self.master.cur.lastrowid
        self.master.conn.commit()
        self.master.cur.execute("SELECT * FROM session WHERE id = ?", (last_row_id,))

        self.master.session = self.master.cur.fetchone()
        self.master.go_camera_main()

    def back_main(self, e):
        self.master.back_main_page()
