import os
import sys
from drawing_map import getImage
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QLineEdit, QPushButton
from get_cor import get_cor

SCREEN_SIZE = [900, 500]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.z = 16
        self.cor = get_cor('Фрязино Ленина 17')
        self.initUI()

    def initUI(self):
        self.mark = []
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.checkBox = QCheckBox(self)
        self.checkBox.setText("Light theme")
        self.checkBox.setGeometry(650, 100, 150, 50)
        self.checkBox.setChecked(True)
        self.checkBox.checkStateChanged.connect(self.uploud_map)
        self.edit = QLineEdit(self)
        self.edit.setText('Finding...')
        self.edit.setGeometry(650, 150, 200, 50)
        self.edit.editingFinished.connect(self.add_mark)
        self.button = QPushButton(self)
        self.button.setText('Delete')
        self.button.setGeometry(650, 200, 200, 50)
        self.button.clicked.connect(self.delete)

        ## Изображение
        self.map_file = getImage(self.cor, self.z, 'light')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)
    def delete(self):
        self.mark = []
        self.uploud_map()
    def add_mark(self):
        if self.edit.text() != 'Finding...' and self.edit.text() != '':
            self.mark.append(get_cor(self.edit.text()))
            self.cor = get_cor(self.edit.text())
            self.uploud_map()

    def keyPressEvent(self, event):
        is_changed = False
        if event.key() == Qt.Key.Key_PageUp:
            self.z += 1
            self.z = min(max(0, self.z), 21)
            is_changed = True
        if event.key() == Qt.Key.Key_PageDown:
            self.z -= 1
            self.z = min(max(0, self.z), 21)
            is_changed = True
        if event.key() == Qt.Key.Key_Up:
            self.cor[1] += 0.001
            is_changed = True
        if event.key() == Qt.Key.Key_Down:
            self.cor[1] -= 0.001
            is_changed = True
        if event.key() == Qt.Key.Key_Right:
            self.cor[0] += 0.001
            is_changed = True
        if event.key() == Qt.Key.Key_Left:
            self.cor[0] -= 0.001
            is_changed = True
        if is_changed:
            self.cor[0] = min(max(self.cor[0], -180), 180)
            self.cor[1] = min(max(self.cor[1], -85), 85)
            self.uploud_map()

    def uploud_map(self):
        os.remove(self.map_file)
        if self.checkBox.isChecked():
            self.map_file = getImage(self.cor, self.z, 'light', self.mark)
        else:
            self.map_file = getImage(self.cor, self.z, 'dark', self.mark)
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
