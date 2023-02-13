import os
import sys

import pygame
import requests


a = input('Координаты через пробел: ').split()
coords = a[1] + ',' + a[0]
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
            if event.key == pygame.K_UP:
                if float(a[0]) + 0.5 > 85:
                    pass
                else:
                    a[0] = float(a[0]) + 0.5
            if event.key == pygame.K_DOWN:
                if float(a[0]) - 0.5 < -85:
                    pass
                else:
                    a[0] = float(a[0]) - 0.5
            if event.key == pygame.K_LEFT:
                if float(a[1]) - 0.5 < -180:
                    a[1] = -float(a[1])
                a[1] = float(a[1]) - 0.5
                print(map_request)
            if event.key == pygame.K_RIGHT:
                if float(a[1]) + 0.5 > 180:
                    a[1] = -float(a[1])
                a[1] = float(a[1]) + 0.5
                print(map_request)
    coords = str(a[1]) + ',' + str(a[0])
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