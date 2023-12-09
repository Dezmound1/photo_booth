import tkinter as tk
from evdev import InputDevice, categorize, ecodes

def power_button_callback(event):
    print("Power button pressed!")

# Найдем устройство кнопки питания (может потребоваться права администратора)
power_button_device_path = None
for device_path in InputDevice.list_devices():
    device = InputDevice(device_path)
    if ecodes.EV_KEY in device.capabilities():
        keys = device.capabilities()[ecodes.EV_KEY]
        if ecodes.KEY_POWER in keys:
            power_button_device_path = device.path
            break

if power_button_device_path:
    # Создаем главное окно Tkinter
    root = tk.Tk()
    root.title("Power Button Listener")

    # Создаем виджет, например, кнопку
    button = tk.Button(root, text="Click me!")
    button.pack()

    # Привязываем обработчик события к кнопке
    button.bind("<Button-1>", power_button_callback)

    # Мониторим устройство кнопки питания
    device = InputDevice(power_button_device_path)
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1 and event.code == ecodes.KEY_POWER:
            power_button_callback(None)

    # Запускаем главный цикл Tkinter
    root.mainloop()
else:
    print("Устройство кнопки питания не найдено.")
