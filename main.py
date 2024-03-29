import sys
import test
import requests
from PIL import Image, ImageQt
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import Qt
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
        self.pushButton.clicked.connect(self.change)
        self.image = QLabel(self)
        self.image.move(100, 15)
        self.image.resize(500, 400)
        self.image.setPixmap(self.pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_W:
            if float(self.scale[0]) <= 59:
                for elem in range(len(self.scale)):
                    ilem = float(self.scale[elem])
                    ilem += ilem / 2
                    self.scale[elem] = str(ilem)
                self.load_map()
        if event.key() == Qt.Key_S:
            if float(self.scale[0]) > 0.000000001:
                for elem in range(len(self.scale)):
                    ilem = float(self.scale[elem])
                    ilem -= ilem / 2
                    self.scale[elem] = str(ilem)
                self.load_map()
        if event.key() == Qt.Key_Y:
            print(self.lat)
            if float(self.lat) <= 80 and float(self.scale[0]) < 45:
                self.lat = str(float(self.lat) + float(self.scale[0]) / 3)
                self.load_map()
        if event.key() == Qt.Key_H:
            if float(self.lat) > -65 and float(self.scale[0]) < 45:
                self.lat = str(float(self.lat) - float(self.scale[0]) / 3)
                self.load_map()
        if event.key() == Qt.Key_J:
            self.lon = str(float(self.lon) + float(self.scale[0]) / 3)
            self.load_map()
        if event.key() == Qt.Key_G:
            self.lon = str(float(self.lon) - float(self.scale[0]) / 3)
            self.load_map()

    # code
    def change(self):
        self.lat = self.coordy.text()
        self.lon = self.coordy_2.text()
        self.scale = [self.zoomindex.text(), self.zoomindex.text()]
        if self.lat == '':
            self.lat = '0'
        if self.lon == '':
            self.lon = '0'
        self.ll = str(self.lon) + "," + str(self.lat)
        print(self.lat)
        print(self.scale)
        if self.scale == ['', '']:
            self.scale = ['0.001', '0.001']
        self.load_map()

    def load_map(self):
        try:
            size1 = f'{self.scale[0]},{self.scale[1]}'
            self.ll = str(self.lon) + "," + str(self.lat)
            print(size1)
            map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&spn={z}&l={type}".format(ll=str(self.ll),
                                                                                              z=str(size1),
                                                                                              type='map')
            response = requests.get(map_request).content
            self.pixmap.loadFromData(response)
            self.image.setPixmap(self.pixmap)
            if not response:
                print("Ошибка выполнения запроса:")
                print(map_request)
                print("Http статус:", response.status_code, "(", response.reason, ")")
                sys.exit(1)
        except Exception:
            print('yoi')

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
        self.size = test.sizer(json_response)

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
            "spn": ",".join([str(self.size[0]), str(self.size[1])]),
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
