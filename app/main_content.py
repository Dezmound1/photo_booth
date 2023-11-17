import flet as ft
from buttons import MainButton, Alert, MainText


class HistoryPage:
    def __init__(self, page, master):
        self.master = master
        self.page = page

        self.title = ft.Text("История сессий", size=30)
        self.button = MainButton("Посмотреть", self.voids)
        self.session_title = MainText("текст сессии")
        self.session_photo = MainText("Фото сессии")
        self.session_comment = MainText("Краткое описание")

        self.button_back = MainButton("Назад", self.back_main)

        self.page.add(
            ft.Row([self.button_back], alignment=ft.MainAxisAlignment.START)
        )

        self.page.add(
            ft.Row(
                [self.title],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        for i in range(5):
            self.session_id = MainText(f"id {i+1}")
            self.page.add(
                ft.Column(
                    [
                        ft.Row(
                            [
                                self.button,
                                self.session_id,
                                self.session_title,
                                self.session_photo,
                                self.session_comment,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                    ]
                )
            )

    def voids(self, e):
        print("do nothing now!")

    def back_main(self, e):
        self.master.new_win(Main)


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
            "Похороны",
            "Я ебу",
            "Мальчишник",
            "Оченьдлинноеслово",
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Похороны",
            "Я ебу",
            "Мальчишник",
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Похороны",
            "Я ебу",
            "Мальчишник",
            "Свадьба",
            "Хелоуин",
            "День рождения",
            "Яблочный спас",
            "Масленница",
            "Похороны",
            "Я ебу",
            "Мальчишник",
        ]

        self.page.add(
            ft.Row(
                [self.button_back],
                alignment=ft.MainAxisAlignment.START,
                visible=True,
            )
        )
        
        row = ft.Row(wrap=False, scroll="AUTO", expand=True, alignment=ft.MainAxisAlignment.CENTER)
        self.page.add(row)
        for i in self.namelist:
                row.controls.append(
                        ft.Container(
                            content=MainText(f'{i}'),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.colors.GREY_600,
                            width=150,
                            height=150,
                            border_radius=10,
                            ink=True,
                            on_click=lambda e: print('boom'),
                        )
                )
        self.page.update()
            

    def void(self, e):
        print("do nothing now!")

    def back_main(self, e):
        self.master.new_win(Main)


class Main:
    def __init__(self, page: ft.Page, master):
        self.master = master
        self.page = page
        self.new_session = Alert(
            event_next=self.list_session, event_close=self.close_dlg
        )
        new = MainButton("Новая", self.open_dlg_modal)
        history = MainButton("История", self.history)
        settings = MainButton("Настройки", self.void)
        shut_down = MainButton("Выключить", self.void)
        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [new],
                        alignment=ft.MainAxisAlignment.CENTER,
                        visible=True,
                    ),
                    ft.Row(
                        [history],
                        alignment=ft.MainAxisAlignment.CENTER,
                        visible=True,
                    ),
                    ft.Row(
                        [settings],
                        alignment=ft.MainAxisAlignment.CENTER,
                        visible=True,
                    ),
                    ft.Row(
                        [shut_down],
                        alignment=ft.MainAxisAlignment.CENTER,
                        visible=True,
                    ),
                ]
            )
        )

    def void(self, e):
        # self.master.new_win()
        print("do nothing now!")

    def history(self, e):
        self.master.new_win(HistoryPage)

    def list_session(self, e):
        if not self.new_session.content.value:
            print(self.new_session.content.value)
            self.new_session.content.error_text = "Нет названия"
            self.page.update()
        else:
            self.close_dlg(e)
            self.master.new_win(SessionList)

    def close_dlg(self, e):
        self.new_session.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.page.dialog = self.new_session
        self.new_session.open = True
        self.page.update()
