import pygame
import sys
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Создание окна (несущественное, поскольку не будет видимого окна)
pygame.display.set_mode((1, 1))

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_POWER]:
                print("dd")
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            print(event.key)
            print(event.mod)
            if event.mod & pygame.K_POWER:
                print("dd")
            if event.key == K_POWER:
                print("Нажата кнопка Power")

    # Задержка для управления частотой обновления
    pygame.time.delay(10)
