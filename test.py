import flet as ft

def main(page: ft.Page):
    page.update()

    def add_container(e):
        # Создание нового контейнера
        new_container = ft.Container(
            content=ft.Text(
                value="00", color="white", size=40, weight="bold", text_align="center"
            ),
            border_radius=30,
            width=70,
            height=70,
            bgcolor=ft.colors.RED,
            opacity=0.5,
        )

        # Создание кнопки для удаления контейнера
        remove_button = ft.ElevatedButton(
            text="Удалить",
            on_click=lambda e: remove_container(new_container, remove_button)
        )

        # Добавление контейнера и кнопки в колонку
        col.controls.extend([new_container, remove_button])
        page.update()

    def remove_container(container, button):
        # Удаление контейнера и кнопки
        col.controls.remove(container)
        col.controls.remove(button)
        page.update()

    # Инициализация главной колонки и кнопки добавления
    col = ft.Column([])
    add_button = ft.ElevatedButton("Добавить", on_click=add_container)

    # Добавление колонки и кнопки на страницу
    page.add(col)
    page.add(add_button)

ft.app(target=main)
