import sys
import main
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.Qt import *
from PIL import Image, ImageOps, ImageFilter


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('program.ui', self)  # Загружаем дизайн
        image = main.main()
        Image.open(image)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
