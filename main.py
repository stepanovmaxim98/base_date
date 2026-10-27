import sqlite3
import sys
import io

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>707</width>
    <height>344</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Фильмы по жанрам</string>
  </property>
  <widget class="QComboBox" name="parameterSelection">
   <property name="geometry">
    <rect>
     <x>10</x>
     <y>10</y>
     <width>161</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QTableWidget" name="tableWidget">
   <property name="geometry">
    <rect>
     <x>180</x>
     <y>10</y>
     <width>511</width>
     <height>311</height>
    </rect>
   </property>
  </widget>
  <widget class="QPushButton" name="queryButton">
   <property name="geometry">
    <rect>
     <x>40</x>
     <y>60</y>
     <width>91</width>
     <height>41</height>
    </rect>
   </property>
   <property name="text">
    <string>Пуск</string>
   </property>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        design = io.StringIO(template)
        uic.loadUi(design, self)
        self.params = {}
        self.con = sqlite3.connect("films_db.sqlite")
        self.select_genres()
        self.queryButton.clicked.connect(self.select)
        self.setWindowTitle('Фильтрация по жанрам')
        self.execute_query_and_fill_table(
            "SELECT title, genre, year FROM films")

    def select_genres(self):
        req = "SELECT * from genres"
        cur = self.con.cursor()
        for value, key in cur.execute(req).fetchall():
            self.params[key] = value
        self.parameterSelection.addItems(list(self.params.keys()))

    def select(self):
        req = (f"SELECT title, genre, year FROM films WHERE genre = "
               f"{self.params.get(self.parameterSelection.currentText())}")
        self.execute_query_and_fill_table(req)

    def execute_query_and_fill_table(self, query):
        cur = self.con.cursor()
        result = cur.execute(query).fetchall()
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setHorizontalHeaderLabels(["Название", "Жанр", "Год"])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
