import os
import sys

import requests
from PyQt5.Qt import Qt
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]
a = input('Координаты через пробел: ').split()
coords = a[1] + ',' + a[0]
z = int(input('Масштаб: '))


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        global coords, z
        map_request = f"http://static-maps.yandex.ru/1.x/?ll={coords}&z={z}&l=map"
        print(map_request)
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def keyPressEvent(self, event):
        global coords, z, a
        if event.key() == Qt.Key_PageDown:
            if z == 0:
                pass
            else:
                z -= 1
        if event.key() == Qt.Key_PageUp:
            if z == 21:
                pass
            else:
                z += 1
        if event.key() == Qt.Key_Up:
            if float(a[0]) + 0.5 > 85:
                pass
            else:
                a[0] = float(a[0]) + 0.5
        if event.key() == Qt.Key_Down:
            if float(a[0]) - 0.5 < -85:
                pass
            else:
                a[0] = float(a[0]) - 0.5
        if event.key() == Qt.Key_Left:
            if float(a[1]) - 0.5 < -180:
                a[1] = -float(a[1])
            a[1] = float(a[1]) - 0.5
        if event.key() == Qt.Key_Right:
            if float(a[1]) + 0.5 > 180:
                a[1] = -float(a[1])
            a[1] = float(a[1]) + 0.5
        coords = str(a[1]) + ',' + str(a[0])
        self.getImage()
        self.initUI()

    def initUI(self):
        print(2)
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())