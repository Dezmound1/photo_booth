import flet as ft
from buttons import MainButton, Alert


class Pages:
    def __init__(self, page):
        self.page = page
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.views = None

        self.new_win(Main)

    def new_win(self, class_name_page):
        if self.views:
            self.views = class_name_page(self.page, self)
        else:
            self.page.clean()
            self.views = class_name_page(self.page, self)
            # clear self,page
            # init class class_name_page

class Main:
    def __init__(self, page: ft.Page, master : Pages):
        self.master = master
        self.page = page
        self.new_session = Alert(event_close=self.close_dlg, event_next=self.close_dlg)
        new = MainButton("Новая", self.open_dlg_modal)
        history = MainButton("История", self.void)
        settings = MainButton("Настройки", self.void)
        shut_down = MainButton("Выключить", self.void)
        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [new], alignment=ft.MainAxisAlignment.CENTER, visible=True
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

    def close_dlg(self, e):
        self.new_session.open = False
        self.page.update()

    def open_dlg_modal(self, e):
        self.page.dialog = self.new_session
        self.new_session.open = True
        self.page.update()



def main(page: ft.Page):
    Pages(page=page)


if __name__ == "__main__":
    ft.app(target=main)
