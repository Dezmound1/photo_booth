import os
import shutil
import psutil

def copy_to_all_usb_drives(source_directory, name_dir):
    # Получить список подключенных флеш-накопителей
    usb_drives = [(partition.device, partition.mountpoint) for partition in psutil.disk_partitions() if partition.fstype == 'vfat' and partition.device.startswith("/dev/sdb")]

    if not usb_drives:
        print("Нет подключенных флеш-накопителей.")
        return

    # Копирование на каждый флеш-накопитель
    for usb_drive, mount_point in usb_drives:
        target_directory = os.path.join(mount_point, name_dir)

        try:
            # Проверка существования папки и создание уникального имени при необходимости
            counter = 1
            while os.path.exists(target_directory):
                target_directory = os.path.join(mount_point, f'{name_dir}_{counter}')
                counter += 1

            # Копирование содержимого исходной папки на флеш-накопитель
            shutil.copytree(source_directory, target_directory)

            print(f"Содержимое скопировано на {usb_drive} в {target_directory}")
        except Exception as e:
            print(f"Ошибка при копировании на {usb_drive}: {e}")

# Замените SOURCE_DIRECTORY на путь к вашей исходной папке
SOURCE_DIRECTORY = './app/templates/Приходит пудж на мид'
name_dir = "Приходит пудж на мид"

# Вызвать функцию для копирования на все подключенные флеш-накопители
copy_to_all_usb_drives(SOURCE_DIRECTORY, name_dir)
