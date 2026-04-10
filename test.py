import os
import sys
from typing import get_origin

from drawing_map import getImage
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QCheckBox, QLineEdit, QPushButton
from get_cor import *

SCREEN_SIZE = [900, 600]


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
        self.text = QLabel(self)
        self.text.setGeometry(50, 450, 600, 50)
        self.checkBox1 = QCheckBox(self)
        self.checkBox1.setText("Show postal code")
        self.checkBox1.setGeometry(650, 250, 150, 50)
        self.checkBox1.setChecked(True)
        self.checkBox1.checkStateChanged.connect(self.update_text)
        self.marktext = ''

        ## Изображение
        self.map_file = getImage(self.cor, self.z, 'light')
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def update_text(self):
        if self.text.text() != '':
            if self.checkBox1.isChecked():
                self.text.setText(get_full_name(self.marktext) + get_postal(self.marktext))
            else:
                self.text.setText(get_full_name(self.marktext))

    def delete(self):
        self.mark = []
        self.text.setText('')
        self.uploud_map()

    def add_mark(self):
        if self.edit.text() != 'Finding...' and self.edit.text() != '':
            self.mark.clear()
            self.mark.append(get_cor(self.edit.text()))
            self.text.setText(get_full_name(self.edit.text()) + get_postal(self.edit.text()))
            self.marktext = self.edit.text()
            self.cor = get_cor(self.edit.text())
            self.uploud_map()

    def keyPressEvent(self, event):
        is_changed = False
        if event.key() == Qt.Key.Key_PageUp or event.key() == Qt.Key.Key_1:
            self.z += 1
            self.z = min(max(0, self.z), 21)
            is_changed = True
        if event.key() == Qt.Key.Key_PageDown or event.key() == Qt.Key.Key_2:
            self.z -= 1
            self.z = min(max(0, self.z), 21)
            is_changed = True
        if event.key() == Qt.Key.Key_Up or event.key() == Qt.Key.Key_W:
            self.cor[1] += 0.00005 * 2 ** (21 - self.z)
            is_changed = True
        if event.key() == Qt.Key.Key_Down or event.key() == Qt.Key.Key_S:
            self.cor[1] -= 0.00005 * 2 ** (21 - self.z)
            is_changed = True
        if event.key() == Qt.Key.Key_Right or event.key() == Qt.Key.Key_D:
            self.cor[0] += 0.00005 * 2 ** (21 - self.z)
            is_changed = True
        if event.key() == Qt.Key.Key_Left or event.key() == Qt.Key.Key_A:
            self.cor[0] -= 0.00005 * 2 ** (21 - self.z)
            is_changed = True
        if is_changed:
            self.cor[0] = min(max(self.cor[0], -180), 180)
            self.cor[1] = min(max(self.cor[1], -85), 85)
            self.uploud_map()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            x = round(self.cor[0] + (event.pos().x() - 300) / 600 * 850 * 2 ** (- self.z), 6)
            y = round(self.cor[1] + (225 - event.pos().y()) / 450 * 395 * 2 ** (- self.z), 6)
            text = str(x) + ',' + str(y)
            self.mark.clear()
            self.mark.append(get_cor(text))
            self.text.setText(get_full_name(text) + get_postal(text))
            self.marktext = text
            self.uploud_map()
        '''if event.button() == Qt.MouseButton.RightButton:
            x = round(self.cor[0] + (event.pos().x() - 300)/600 *850* 2 ** ( - self.z), 6)
            y = round(self.cor[1] + (225 -event.pos().y())/450 * 395*2 ** ( - self.z), 6)
            text = str(x) + ',' + str(y)
            name, coor = find_org(text, self.edit.text())
            print(name, coor)
            self.mark.clear()
            self.mark.append(coor)
            self.text.setText(get_full_name(text) + get_postal(text))
            self.marktext = text
            self.uploud_map()'''

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
