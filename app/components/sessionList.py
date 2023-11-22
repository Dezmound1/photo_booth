import flet as ft
from components.buttons import MainButton, MainText


class SessionList:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.button_back = MainButton("Назад", self.back_main)
        self.namelist = [
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Мальчишник",
            "Оченьдлинноеслово",
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Мальчишник",
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Мальчишник",
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Мальчишник",
        ]
        # self.title = ft.Text(self.title, size=30)
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
        self.master.back_user_choise(name)

    def back_main(self, e):
        self.master.back_main_page()
