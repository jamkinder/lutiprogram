import requests

def sizer(geodata):
    LC = geodata['response']['GeoObjectCollection']['featureMember']
    LC = LC[0]
    LC = LC['GeoObject']['boundedBy']['Envelope']['lowerCorner']
    UP = geodata['response']['GeoObjectCollection']['featureMember']
    UP = UP[0]
    UP = UP['GeoObject']['boundedBy']['Envelope']['upperCorner']
    LC = LC.split(' ')
    UP = UP.split(' ')
    dd = float(UP[0]) - float(LC[0]), float(UP[1]) - float(LC[1])
    return dd