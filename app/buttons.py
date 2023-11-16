import flet as ft
from flet import Container


class MainButton(Container):
    def __init__(self, text, on_click):
        super().__init__()
        self.content = ft.ElevatedButton(
            content=ft.Column(
                [ft.Text(value=text, size=20)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            height=50,
            width=200,
            on_click=on_click,
        )


class MainText(ft.Text):
    def __init__(self, value: str):
        super().__init__()
        self.value = value
        self.size = 20


class Alert(ft.AlertDialog):
    def __init__(self, event_next, event_close, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.modal = True
        self.title = ft.Text("Новая сессия")
        self.content = ft.TextField(label="Введите название")
        self.actions = [
            ft.TextButton("Подтвердить", on_click=event_next),
            ft.TextButton("Назад", on_click=event_close),
        ]
        self.actions_alignment = ft.MainAxisAlignment.CENTER
