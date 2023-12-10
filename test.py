import tkinter as tk
import subprocess

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My App")

        # Ваш код для создания основного интерфейса приложения

        # Кнопка для запуска виртуальной клавиатуры
        btn_open_keyboard = tk.Button(root, text="Открыть клавиатуру", command=self.open_keyboard)
        btn_open_keyboard.pack()

    def open_keyboard(self):
        try:
            subprocess.Popen(['onboard'])
        except Exception as e:
            print(f"Error launching onboard: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()
O
