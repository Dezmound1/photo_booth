import flet as ft
from buttons import MainButton, Alert, MainText
from time import sleep


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
            ft.Container(
                content=self.button_back, alignment=ft.alignment.top_left
            )
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

    def back_main(self, e):
        self.master.new_win(Main)

    def voids(self, e):
        print("aaa")


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

        self.row = ft.GridView(
            expand=True,
            runs_count=4
        )
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
        self.master.new_win(UserChoise, name)

    def back_main(self, e):
        self.master.new_win(Main)


class UserChoise:
    def __init__(self, page, master, name):
        self.master = master
        self.page = page
        self.name_category = name
        self.cards = ft.Row(
            wrap=False,
            scroll="AUTO",
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.add(
            ft.Row(
                [
                    ft.Text(
                        self.name_category,
                        style=ft.TextThemeStyle.DISPLAY_MEDIUM,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.add(self.cards)

        for i in range(5):
            self.cards.controls.append(
                ft.Container(
                    content=MainText(f"CARD {i}"),
                    margin=10,
                    padding=10,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.GREY_600,
                    width=420,
                    height=1080,
                    border_radius=15,
                    ink=True,
                    on_click=self.photo_maker,
                )
            )
            self.page.update()

    def photo_maker(self, e):
        self.master.new_win(PhotoPage, self.name_category)


class PhotoPage:
    def __init__(self, page, master, name):
        self.page = page
        self.master = master
        self.count = 1
        self.name_category = name

        self.button = MainButton("Создать", self.void)
        self.colum = ft.Column(
            controls=[
                ft.Text(
                    value="YOUR PHOTO",
                    size=40,
                    font_family="RobotoSlab",
                    weight=ft.FontWeight.W_600,
                ),
            ],
            horizontal_alignment=ft.MainAxisAlignment.CENTER,
        )
        self.page.add(
            ft.Row(
                [
                    self.colum,
                    self.button,
                    ft.Column(
                        controls=[
                            MainButton("Назад", lambda e: self.back(e, name))
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
            )
        )

    def void(self, e):
        if self.count < 5:
            self.count += 1
            self.colum.controls.append(
                ft.Container(
                    ft.Stack(
                        [
                            ft.Container(
                                margin=10,
                                right=0,
                                border_radius=5,
                                width=70,
                                height=70,
                                content=ft.IconButton(
                                    icon=ft.icons.DELETE_FOREVER_ROUNDED,
                                    icon_color="pink600",
                                    icon_size=40,
                                    tooltip="Удалить фотографию",
                                ),
                            )
                        ]
                    ),
                    border_radius=8,
                    padding=5,
                    width=400,
                    height=250,
                    bgcolor=ft.colors.BLACK,
                )
            )
            self.page.update()
        else:
            self.button.visible = False
            self.page.controls[0].controls[1] = MainButton(
                "Сформировать", on_click=self.to_print
            )
            self.page.update()
            # self.page.add()

    def back(self, e, name):
        self.master.new_win(UserChoise, name)

    def to_print(self, e):
        self.master.new_win(PrintPage)


class PrintPage:
    def __init__(self, page, master):
        self.page = page
        self.master = master
        page.title = "Print your photo"
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.txt_number = ft.TextField(
            value="0", text_align="right", width=400, text_size=30
        )

        self.page.add(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                border_radius=8,
                                padding=5,
                                width=420,
                                height=700,
                                bgcolor=ft.colors.BLACK,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.icons.REMOVE,
                                on_click=self.minus_click,
                                icon_size=50,
                            ),
                            self.txt_number,
                            ft.IconButton(
                                ft.icons.ADD,
                                on_click=self.plus_click,
                                icon_size=50,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            )
        )

    def minus_click(self, e):
        if self.txt_number.value == "0":
            self.txt_number.value = "0"
        else:
            self.txt_number.value = str(int(self.txt_number.value) - 1)
            self.page.update()

    def plus_click(self, e):
        if self.txt_number.value == "8":
            self.txt_number.value = "8"
        else:
            self.txt_number.value = str(int(self.txt_number.value) + 1)
            self.page.update()


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
        shut_down = MainButton("Выключить", self.shut_down)
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
            sleep(.3)
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
