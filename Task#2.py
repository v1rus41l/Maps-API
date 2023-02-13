import os
import sys

import pygame
import requests


coords = input('Координаты через пробел: ').split()
coords = coords[1] + ',' + coords[0]
print(coords)
z = int(input('Масштаб: '))
map_request = f"https://static-maps.yandex.ru/1.x/?l=map&ll={coords}&z={z}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if z == 21:
                    pass
                else:
                    z += 1
                print(map_request)
            if event.key == pygame.K_PAGEDOWN:
                if z == 0:
                    pass
                else:
                    z -= 1
                print(map_request)
    map_request = f"https://static-maps.yandex.ru/1.x/?l=map&ll={coords}&z={z}"
    response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
os.remove(map_file)