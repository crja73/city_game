import pygame
import sys
from func import parameters
import requests
import pygame
import os
from geocoder import get_coordinates, get_nearest_object
import random
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton
from PyQt5.QtWidgets import QInputDialog
 


number = 1


spis_of_cities = ['Москва', 'Париж', 'Нижний Новгород', 'Шанхай', 'London', 'New-York', 'Denver', 'Киев', 'Оттава']

toponym_to_find = random.choice(spis_of_cities)

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:

    pass

json_response = response.json()

toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]

toponym_coodrinates = toponym["Point"]["pos"]

toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

map_params = parameters(toponym_longitude, toponym_lattitude)
map_api_server = "http://static-maps.yandex.ru/1.x/"

response = requests.get(map_api_server, params=map_params)



map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

if number % 2 == 0:
	print('ходит игрок # 1')
else:
	print('ходит игрок # 2')
number += 1
pygame.init()
screen = pygame.display.set_mode((600, 450))
BLACK = 0, 0, 0

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button_1 = QPushButton(self)
        self.button_1.move(40, 40)
        self.button_1.setText("Угадать город")
        self.button_1.clicked.connect(self.run)

        self.show()

    def run(self):
        i, okBtnPressed = QInputDialog.getItem(self, "Выберите город", 
                                       "Что за город на картинке?", 
                                       ('Москва', 'Париж', 'Нижний Новгород', 'Шанхай', 'London', 'New-York', 'Denver', 'Киев', 'Оттава'), 
                                       1, False)
        if okBtnPressed:     
            if toponym_to_find == i:
            	print('Ты победил')
            	if number % 2 == 0:
            		gamer1 += 1
            	else:
            		gamer2 += 1
            else:
            	print('Ты проиграл, это {}'.format(toponym_to_find))

screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()

   
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
  
os.remove(map_file)
print('очков у игрока 1: {}'.format(gamer1))
print('очков у игрока 2: {}'.format(gamer2))