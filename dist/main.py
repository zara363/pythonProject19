import sys
import sqlite3
import io

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QTableWidgetItem, QPushButton, QMessageBox

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QInputDialog

qpt = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>896</width>
    <height>721</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushBtn">
    <property name="geometry">
     <rect>
      <x>310</x>
      <y>120</y>
      <width>91</width>
      <height>23</height>
     </rect>
    </property>
    <property name="text">
     <string>Поиск</string>
    </property>
   </widget>
   <widget class="QComboBox" name="box1">
    <property name="geometry">
     <rect>
      <x>190</x>
      <y>50</y>
      <width>121</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
   <widget class="QComboBox" name="box2">
    <property name="geometry">
     <rect>
      <x>400</x>
      <y>50</y>
      <width>121</width>
      <height>22</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>400</x>
      <y>20</y>
      <width>131</width>
      <height>16</height>
     </rect>
    </property>
    <property name="text">
     <string>Укажите размер платья</string>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>190</x>
      <y>20</y>
      <width>121</width>
      <height>21</height>
     </rect>
    </property>
    <property name="text">
     <string>Укажите цвет платья</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>170</y>
      <width>791</width>
      <height>301</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="order_btn">
    <property name="geometry">
     <rect>
      <x>610</x>
      <y>610</y>
      <width>141</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>Посмотреть покупки</string>
    </property>
   </widget>
   <widget class="QTableWidget" name="tableWidget_2">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>480</y>
      <width>561</width>
      <height>181</height>
     </rect>
    </property>
   </widget>
   <widget class="QPushButton" name="busket_button">
    <property name="geometry">
     <rect>
      <x>610</x>
      <y>490</y>
      <width>141</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>Открыть корзину</string>
    </property>
   </widget>
   <widget class="QPushButton" name="busket_button_2">
    <property name="geometry">
     <rect>
      <x>610</x>
      <y>550</y>
      <width>141</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>Купить товар</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>896</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        f = io.StringIO(qpt)
        #Загружаем ui файл
        uic.loadUi(f, self)
        self.setWindowTitle('Figure skating dresses')

        #Подключаемся к базе данных
        self.connection = sqlite3.connect("rent_dresses")
        self.pushBtn.clicked.connect(self.select_products)
        #Добавляем в QComboBox элементы
        self.box1.addItems(['red', 'purple', 'blue', 'black'])
        self.box2.addItems(['s', 'xs'])

        self.box1.activated[str].connect(self.catch_col)
        self.box2.activated[str].connect(self.catch_size)

        self.size = 's'
        self.color = 'red'
        #Создаем кнопку для поиска подходящих вариантов
        self.btn_pic = QPushButton(self)
        self.btn_pic.move(1000, 1000)

        self.i = 180
        self.initUI()

        self.buy_btn = QPushButton(self)
        self.buy_btn.move(1000, 1000)
        self.buy_btn.resize(5, 5)

        self.add_busket = QPushButton(self)
        self.add_busket.move(1000, 1000)
        self.add_busket.resize(5, 5)

        self.busket_button_2.clicked.connect(self.buy_item)

        # Устанавливаем цвет кнокпи
        self.busket_button_2.setStyleSheet(
            "background-color: plum;")

        #Устанавливаем цвет фона
        self.setStyleSheet(
            "background-color: lavender;")

        #Устанавливаем цвет кнопки
        self.pushBtn.setStyleSheet(
            "background-color: plum;")

        self.order_btn.clicked.connect(self.show_order)
        self.order_btn.setStyleSheet(
            "background-color: plum;")

        self.busket_button.clicked.connect(self.add_funct)
        #Устанавливаем цвет кнопки для корзины
        self.busket_button.setStyleSheet(
            "background-color: plum;")

        #Список, в который мы будем добавлять платья,
        # которые клиент решил добавить в корзину
        self.add_b = []
        self.a = 1

    def initUI(self):
        #Создаем поле для нашего изображения
        self.image = QLabel(self)
        #Создаем кнопку для удаления изображения
        self.delete_btn = QPushButton(self)
        self.delete_btn.resize(5, 5)
        self.delete_btn.move(700, 700)

    def select_products(self):
        try:
            cur = self.connection.cursor()
            #Получаем результат запроса, на основе данных, которые ввел пользователь
            result = cur.execute(f'SELECT name as dresstype, price, size '
                             f'FROM products '
                             f'WHERE size = "{self.size}" '
                             f'AND color=(SELECT id FROM colors '
                             f'WHERE color = "{self.color}") '
                             f'AND available = "Yes"').fetchall()
            #Если таких платьев не нашлось, то очищаем нашу таблицу
            if not result:
                self.tableWidget.clear()
            self.name_dress = result[0][0]
            self.size = result[0][2]
            self.price = result[0][1]

            #Получаем id платья
            res2 = cur.execute(f'SELECT id FROM products '
                               f'WHERE size = "{self.size}" '
                               f'AND color=(SELECT id FROM colors '
                               f'WHERE color = "{self.color}") '
                               f'AND available = "Yes"').fetchall()
            self.id = res2[0][0]
            self.resultat = (self.name_dress, self.size, self.price)
            self.info = (self.name_dress, self.size, self.price)

            #Заполняем размеры таблицы
            self.tableWidget.setColumnCount(3)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(
                ['Название платья', 'цена товара', 'размер'])
            #Устанавливаем фиксированный размер столбцов
            self.tableWidget.horizontalHeader().setDefaultSectionSize(130)

            #Заполняем таблицу полученными элементами
            for i, row in enumerate(result):
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for k, elem in enumerate(row):
                    self.tableWidget.setItem(i, k, QTableWidgetItem(str(elem)))
            #Вызываем функции для показа изображения и покупки
            self.make_btn()
            self.buy_button()
            self.bus()

        #Рассматриваем вариант, если по выбранным критериям не нашлось платьев
        except Exception:
            announcement = QMessageBox.question(self, 'Магазин аренды платьев',
                                                "К сожалению таких платьев не нашлось",
                                            buttons=QMessageBox.Ok | QMessageBox.Cancel)

    def make_btn(self):
        #Создаем изображение, запрошенного платья
        self.btn_pic.setText('Посмотреть изображение')
        self.btn_pic.setStyleSheet(
            "background-color: plum;")

        self.btn_pic.move(460, 180)
        self.btn_pic.resize(140, 25)

        self.btn_pic.clicked.connect(self.show_pic)

    def catch_col(self, text):
        #Фиксируем цвет платья, который нужен пользователю
        self.color = text

    def show_pic(self):
        #Выводим картинку на экран
        cur = self.connection.cursor()
        res = cur.execute(f'SELECT image FROM products '
                          f'WHERE id = {self.id}').fetchall()

        pixmap = QPixmap(res[0][0])
        #Устанавливаем размеры картинки
        self.image.move(430, 225)
        self.image.resize(230, 240)
        self.image.setPixmap(pixmap)

        #Устанавливаем конпку для закрытия картинки
        self.delete_btn.setText('X')
        self.delete_btn.move(590, 225)
        self.delete_btn.resize(30, 30)

        #Устанавливаем цвет кнопки
        self.delete_btn.setStyleSheet(
            "background-color: white;")
        self.delete_btn.clicked.connect(self.delete_button)

    def buy_button(self):
        #Создаем кнопку для приобретения платья
        self.buy_btn.setText('Приобрести')

        #Устанавливаем размеры кнопки
        self.buy_btn.move(620, 180)
        self.buy_btn.resize(90, 25)
        self.buy_btn.clicked.connect(self.confirmation_btn)

        self.buy_btn.setStyleSheet(
                "background-color: plum;")

    def bus(self):
        #Добавляем кнопку для добавления в корзину
        self.add_busket.setText('Добавить в корзину')

        #Устанавливаем размеры кнопки
        self.add_busket.move(727, 180)
        self.add_busket.resize(115, 25)

        #Устанавливаем цвет кнопки
        self.add_busket.setStyleSheet(
            "background-color: plum;")
        self.add_busket.clicked.connect(self.add_product)

    def confirmation_btn(self):
        #Запрашиваем подтверждение на покупку
        confirm = QMessageBox.question(self, 'Магазин аренды платьев',
                                       "Вы действительно хотите приобрести данное платье?",
                                       buttons=QMessageBox.Yes | QMessageBox.No)

        #Рассматриваем случай, если клиент желает купить данный товар
        if confirm == QMessageBox.Yes:
            self.get_name()

    def get_name(self):
        #Запрос на ввод имени пользователя
        name, ok_pressed = QInputDialog.getText(self, "Введите имя",
                                                "Введите своё имя?")
        if ok_pressed:
            #Фиксируем имя покупателя
            self.name = name
            self.info = [self.name, self.name_dress, self.size, str(self.price)]

            cur = self.connection.cursor()

            #Добавляем имя пользователя и информацию о платье, которе он купил, в таблицу покупателей
            cur.execute(f'INSERT INTO customers(customer_id, username, dress_name, dress_size) '
                        f'VALUES({self.id}, "{self.name}", "{self.name_dress}", "{self.size}")')

            #Заменяем в таблице каталога платьев доступность на недоступность данного товара
            cur.execute(f'UPDATE products '
                        f'SET available = "No" '
                        f'WHERE id = "{self.id}"')

            #Сохраняем изменения
            self.connection.commit()
            self.end_purchase()
            #Вызываем функцию для записи в файл
            self.write_file()

    def end_purchase(self):
        #Объявление об успешной покупке
        announcement = QMessageBox.question(self, 'Магазин аренды платьев',
                                            "Спасибо, что выбрали нас!",
                                            buttons=QMessageBox.Ok | QMessageBox.Cancel)
        if announcement == QMessageBox.Ok:
            pass

    def delete_button(self):
        self.delete_btn.move(1000, 1000)
        #Закрытие изображения по нажатию на кнопку
        self.image.clear()

    def catch_size(self, text):
        self.size = text

    def show_order(self):
        try:
            cur = self.connection.cursor()
            #Ищем информацию о покупках покупателя
            result = cur.execute(f'SELECT username, dress_name, dress_size '
                                 f'FROM customers '
                                 f'WHERE username = "{self.name}"').fetchall()

            #Устанавливаем размеры таблицы
            self.tableWidget_2.setColumnCount(3)
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.horizontalHeader().setDefaultSectionSize(150)

            #Устанавливаем названия столбцов
            self.tableWidget_2.setHorizontalHeaderLabels(['Имя пользователя', 'Название платья', 'Размер платья'])

            #Заполняем таблицу
            for i, row in enumerate(result):
                self.tableWidget_2.setRowCount(self.tableWidget_2.rowCount() + 1)
            for k, elem in enumerate(row):
                self.tableWidget_2.setItem(i, k, QTableWidgetItem(str(elem)))

        #Рассмотрим вариант, если пользователь еще не совершал покупок
        except Exception:
            announcement = QMessageBox.question(self, 'Магазин аренды платьев',
                                                'Вы еще не совершали покупок',
                                                buttons=QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
            if announcement == QMessageBox.Ok:
                pass

    def add_product(self):
        #Добавляем продукт в корзину
        self.add_b.append(self.resultat)
        self.kpop()

    def kpop(self):
        #Удаляем лишние элементы
        k = self.add_b
        for i in k:
            if k.count(i) > 1:
                k.remove(i)
        self.add_b = k

    def add_funct(self):
        self.tableWidget_2.clear()

        #Устанавливаем размеры таблицы
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setRowCount(0)

        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(150)

        #Устанавливаем названия колонок
        self.tableWidget_2.setHorizontalHeaderLabels(['Название платья', 'Размер платья', 'Цена платья'])

        #Заполняем данные в таблице
        for i, row in enumerate(self.add_b):

            #Добавляем ячейку
            self.tableWidget_2.setRowCount(self.tableWidget_2.rowCount() + 1)
            for k, elem in enumerate(row):
                self.tableWidget_2.setItem(i, k, QTableWidgetItem(str(elem)))

    def buy_item(self):
        #Получаем выделенную информацию из таблицы
        rows = list([i.text() for i in self.tableWidget_2.selectedItems()])

        self.name_dress = rows[0]
        self.size = rows[1]
        self.price = rows[2]
        self.price = int(self.price)

        self.get_info()

    def get_info(self):
        cur = self.connection.cursor()
        #Находим id подходящего платья
        res2 = cur.execute(f'SELECT id FROM products '
                           f'WHERE size = "{self.size}" '
                           f'AND name = "{self.name_dress}" '
                           f'AND available = "Yes"').fetchall()
        #Фиксируем id платья
        self.id = res2[0][0]
        #Вызываем функцию для подтверждения покупки
        self.confirmation_btn()

    def write_file(self):
        #Записываем информацию о покупателе и платье, которое он купил
        f = open("dress_write.txt", 'a')
        f.writelines(' '.join(self.info))

        #Закрываем файл
        f.close()

    def dress_info(self):
        r = self.info


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())