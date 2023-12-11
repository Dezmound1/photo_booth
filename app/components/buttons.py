import flet as ft
from flet import Container


class MainButton(Container):
    def __init__(self, text, on_click):
        super().__init__()
        self.content = ft.ElevatedButton(
            content=ft.Column(
                [ft.Text(value=text, size=26)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=70,
            width=250,
            on_click=on_click,
        )


class RedButton(Container):
    def __init__(self, text, on_click):
        super().__init__()
        self.content = ft.ElevatedButton(
            content=ft.Column(
                [ft.Text(value=text, size=26)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=70,
            width=250,
            style=ft.ButtonStyle(
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.RED),
                    ft.MaterialState.HOVERED: ft.BorderSide(1, ft.colors.BLACK),
                },
                color={ft.MaterialState.HOVERED: ft.colors.GREY_800},
                animation_duration=250,
            ),
            on_click=on_click,
        )


class MainText(ft.Text):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
        self.size = 30
        self.text_align = ft.TextAlign.CENTER


class Alert(ft.AlertDialog):
    def __init__(self, event_next, event_close, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modal = True
        self.title = MainText("Новая сессия")
        self.content = ft.TextField(
            label="Введите название", autofocus=True, width=700
        )
        self.actions = [
            MainButton("Подтвердить", on_click=event_next),
            MainButton("Назад", on_click=event_close),
        ]
        self.actions_alignment = ft.MainAxisAlignment.CENTER


class BackButton(Container):
    def __init__(self, text, on_click):
        super().__init__()
        self.content = ft.ElevatedButton(
            content=ft.Column(
                [ft.Text(value=text, size=26)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=40,
            width=150,
            style=ft.ButtonStyle(
                side={
                    ft.MaterialState.DEFAULT: ft.BorderSide(1, ft.colors.RED),
                    ft.MaterialState.HOVERED: ft.BorderSide(1, ft.colors.BLACK),
                },
                color={ft.MaterialState.HOVERED: ft.colors.GREY_800},
                animation_duration=250,
            ),
            on_click=on_click,
        )
