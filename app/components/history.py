import flet as ft
from components.buttons import MainButton, MainText



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

        self.page.add(ft.Container(content=self.button_back, alignment=ft.alignment.top_left))
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

    def back_main(self, e):
        self.master.back_main_page()

    def voids(self, e):
        print("aaa")
