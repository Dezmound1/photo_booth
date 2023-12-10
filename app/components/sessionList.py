import flet as ft

import os
from datetime import datetime

from components.buttons import MainButton, MainText, RedButton


class SessionList:
    def __init__(self, page, master, name):
        self.master = master
        self.page = page
        self.name = name

        self.namelist = os.listdir("./templates")
        try:
            self.namelist.remove("test_img")
        except:
            pass

        self.button_back = MainButton("Назад", self.back_main)
        self.page.add(
            ft.Row(
                [self.button_back],
                alignment=ft.MainAxisAlignment.START,
                visible=True,
            )
        )

        self.row = ft.GridView(expand=True, runs_count=4)
        self.page.add(self.row)
        for i in self.namelist:
            self.row.controls.append(self.creat_buttom(i))
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
            ink=True,
            on_click=lambda e: self.userlist(e, name),
        )

    def userlist(self, e, name):
        date = str(datetime.now().date())
        name_dir = "./photo_session/" + self.name + "_" + date
        os.makedirs(name_dir)
        os.makedirs(name_dir + "/photo")
        os.makedirs(name_dir + "/photo_templates")

        self.master.cur.execute(
            "INSERT INTO session (name, date, dir, topic) VALUES (?, ?, ?, ?)", (self.name, date, name_dir, name)
        )
        last_row_id = self.master.cur.lastrowid
        self.master.conn.commit()
        self.master.cur.execute("SELECT * FROM session WHERE id = ?", (last_row_id,))

        self.master.session = self.master.cur.fetchone()
        self.master.user_choise()

    def back_main(self, e):
        self.master.back_main_page()
