import sys
import test
import requests
from PIL import Image, ImageQt
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5 import QtCore
from PyQt5.QtGui import QPainter, QColor, QPixmap, QImage
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog, QLabel, QFileDialog
import PyQt5


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('program.ui', self)  # Загружаем дизайн
        global im1
        self.fname = ''
        self.main()
        self.curr_image = QImage
        self.image = QLabel(self)
        self.image.move(100, 15)
        self.image.resize(500, 400)
        self.image.setPixmap(self.pixmap)

    def main(self):
        # Пусть наше приложение предполагает запуск:
        # python search.py Москва, ул. Ак. Королева, 12
        # Тогда запрос к геокодеру формируется следующим образом:
        toponym_to_find = " ".join(sys.argv[1:])

        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}

        response = requests.get(geocoder_api_server, params=geocoder_params)

        if not response:
            # обработка ошибочной ситуации
            pass

        # Преобразуем ответ в json-объект

        json_response = response.json()
        size = test.sizer(json_response)

        # Получаем первый топоним из ответа геокодера.
        toponym = json_response["response"]["GeoObjectCollection"][
            "featureMember"][0]["GeoObject"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"]

        # Долгота и широта:
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join([str(size[0]), str(size[1])]),
            "l": "map",
            "pt": "{0},pm2dgl".format(','.join(toponym_coodrinates.split()))
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params).content
        self.pixmap = QPixmap()
        self.pixmap.loadFromData(response)
        # Создадим картинку
        # и тут же ее покажем встроенным просмотрщиком операционной системы


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
