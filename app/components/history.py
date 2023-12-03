import flet as ft
from components.buttons import MainButton, MainText


class HistoryPage:
    def __init__(self, page, master):
        self.master = master
        self.page = page
        self.master.cur.execute("SELECT * FROM session")
        self.list_session = self.master.cur.fetchall()

        self.title = ft.Text("История сессий", size=30)
        self.session_comment = MainText("Краткое описание")

        self.button_back = MainButton("Назад", self.back_main)
        
        self.lv = ft.ListView(expand=1)

        self.page.add(ft.Container(content=self.button_back, alignment=ft.alignment.top_left))
        self.page.add(
            ft.Row(
                [self.title],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.add(
            self.lv
        )
        for i in self.list_session:
            self.creat_row(i)
            self.page.update()

    def creat_row(self, session):
        self.lv.controls.append(
            ft.Column(
                [
                    ft.Row(
                        [
                            MainText(str(session[0])),
                            MainText(session[3].split("/")[-1]),
                            MainText(session[4]),
                            MainButton("Продолжить", lambda e: self.resume_session(e, session[0])),
                            MainButton("Фотографии", lambda e: self.photo_session(e, session[0])),
                            MainButton("Удалить", lambda e: self.del_session(e, session[0])),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    ),
                ]
            )
        )

    def back_main(self, e):
        self.master.back_main_page()
        
    def del_session(self,e,session_id):
        self.master.cur.execute("DELETE FROM session WHERE id = ?", (session_id,))
        self.master.conn.commit()
        self.master.new_win(HistoryPage)

    def photo_session(self,e,session_id):
        self.master.cur.execute('SELECT * FROM session WHERE id = ?', (session_id,))
        self.master.session = self.master.cur.fetchone()
    
    def resume_session(self,e,session_id):
        self.master.cur.execute('SELECT * FROM session WHERE id = ?', (session_id,))
        self.master.session = self.master.cur.fetchone()
        self.master.user_choise()
