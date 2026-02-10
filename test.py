import os
import sys
from drawing_map import getImage
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from get_cor import get_cor

SCREEN_SIZE = [700, 500]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.z = 16
        self.cor = get_cor('Фрязино Ленина 17')
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.map_file = getImage(self.cor, self.z, 'dark')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp:
            self.z += 1
            self.z = min(max(0, self.z), 21)
            self.uploud_map()
        if event.key() == Qt.Key.Key_PageDown:
            self.z -= 1
            self.z = min(max(0, self.z), 21)
            self.uploud_map()
        if event.key() == Qt.Key.Key_Up:
            self.cor[1] += 0.001
            self.uploud_map()
        if event.key() == Qt.Key.Key_Down:
            self.cor[1] -= 0.001
            self.uploud_map()
        if event.key() == Qt.Key.Key_Right:
            self.cor[0] += 0.001
            self.uploud_map()
        if event.key() == Qt.Key.Key_Left:
            self.cor[0] -= 0.001
            self.uploud_map()

    def uploud_map(self):
        os.remove(self.map_file)
        self.map_file = getImage(self.cor, self.z, 'dark')
        self.pixmap = QPixmap(self.map_file)
        self.image.clear()
        self.image.setPixmap(self.pixmap)
        self.update()

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
