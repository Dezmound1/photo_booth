#!/usr/bin/env python

from evdev import InputDevice, categorize, ecodes
import subprocess

def main():
    device_path = '/dev/input/event2'  # Поменяйте на путь к вашему устройству
    device = InputDevice(device_path)

    print(f"Monitoring events on {device_path}")

    for event in device.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            # Обрабатываем только нажатия клавиш (EV_KEY) с состоянием 1 (нажата)
            print(f"Key {categorize(event).keycode} pressed")

            # Здесь вы можете выполнить нужные вам действия.
            # Например, запустить ваш скрипт
            subprocess.run(['./btn.sh'])

if __name__ == "__main__":
    main()
