import flet as ft
from components.buttons import MainButton, Alert, RedButton
from time import sleep
from components.sessionList import SessionList
from components.history import HistoryPage
from components.settings_page import Settings

class Main:
    def __init__(self, page: ft.Page, master):
        self.master = master
        self.page = page

        self.new_session = Alert(event_next=self.list_session, event_close=self.close_dlg)
        new = MainButton("Новая", self.open_dlg_modal)
        history = MainButton("История", self.history)
        settings = MainButton("Настройки", self.settings)
        shut_down = RedButton("Выключить", self.shut_down)
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
                ],
                spacing=20,
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
            r = self.new_session.content.value
            print(type(r), r)
            self.close_dlg(e)
            sleep(0.3)
            self.master.new_win(SessionList)

    def close_dlg(self, e):
        self.new_session.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.page.dialog = self.new_session
        self.new_session.open = True
        self.page.update()

    def shut_down(self, e):
        self.page.window_destroy()
    
    def settings(self, e):
        self.master.new_win(Settings)
