#!/bin/bash

# Получаем список всех USB-принтеров
printers=$(lpinfo -v | grep -i usb | awk '{print $2}')

# Переменная для подсчета добавленных принтеров
count=0

# Перебираем каждый принтер
for uri in $printers; do
    # Генерируем имя принтера
    name="USBPrinter_$count"

    # Добавляем принтер
    echo "Добавление принтера: $name"
    lpadmin -p "$name" -E -v "$uri" -m gutenprint.5.3://dnp-dsrx1/expert

    # Применяем специфическую настройку размера страницы
    echo "Применение настройки PageSize=w288h432-div2 к принтеру: $name"
    lpadmin -p "$name" -o PageSize=w288h432-div2
    lpadmin -d "$name"
    # Увеличиваем счетчик
    ((count++))
done

# Выводим общее количество добавленных принтеров
echo "Добавлено принтеров: $count"
