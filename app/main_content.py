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


class Main:
    def __init__(self, page: ft.Page, master):
        self.master = master
        self.page = page
        self.new_session = Alert(
            event_close=self.close_dlg, event_next=self.close_dlg
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

    def close_dlg(self, e):
        self.new_session.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.page.dialog = self.new_session
        self.new_session.open = True
        self.page.update()
