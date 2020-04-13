from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton,
                             QTableView, QVBoxLayout, QHBoxLayout)
from PyQt5.QtCore import QCoreApplication
from handlers import Dialog
from requests import query1, query2, query3, get_goods, get_purchases, add_branch, max_budget
from PyQt5.QtWidgets import (QLineEdit, QDialog, QDialogButtonBox, QComboBox,
                             QFormLayout, QLabel, QSpinBox, QRadioButton,QTextBrowser)
# from app import Session

DESCRIPTION_1 = "Руководители отделов, закупивших предмет типа Х"
DESCRIPTION_2 = "Реквизиты поставщиков, поставляющих предметы для проекта X,\n\
отсортированные по кол-ву предметов в закупке"
DESCRIPTION_3 = "Адреса филиалов, виды предметов и названия проектов с бюджетом не менее Х,\n\
для которых поставляется оборудование, название которго содержит подстроку Y"


class MainWindow(QMainWindow):

    def __init__(self):
        # MainWindow главное окно приложения
        super().__init__()
        # окно для вывода
        # self._view = QTableView()
        self._view = QTextBrowser()
        # инициализация кнопок
        self._buttonAdd = QPushButton("Добавить")
        self._quit = QPushButton('Закончить')
        self._buttons = [(QPushButton("Первый запрос"), self.query_1),
                         (QPushButton("Второй запрос"), self.query_2),
                         (QPushButton("Третий запрос"), self.query_3)]

    def init_ui(self):
        # Класс QWidget является базовым для всех объектов пользовательского интерфейса.
        # Виджет - это элементарный объект пользовательского интерфейса:
        # он получает события мыши, клавиатуры и другие события от оконной системы и рисует свое изображение на экране.
        widget = QWidget()
        # Класс QVBoxLayout Выстраивает виджеты в вертикальную линию.
        main_layout = QVBoxLayout()
        # Класс QHBoxLayout выстраивает виджеты в горизонтальную линию.
        tmp_layout = QHBoxLayout()
        # соединение кнопки и функции
        self._buttonAdd.clicked.connect(self.add_to_db)
        # соединение кнокпи "Закончить" c сигналом выхода
        self._quit.clicked.connect(QCoreApplication.instance().quit)
        # соединение копок для запросов с функциями запросов
        for button, handler in self._buttons:
            button.clicked.connect(handler)
        # размер окна
        self.setGeometry(400, 400, 300, 300)
        # название окна
        self.setWindowTitle('Наш курсовой проект')
        # установка в главном оне вертикаольного лейата
        widget.setLayout(main_layout)
        # Устанавливает заданный виджет (widget), в качестве центрального виджета главного окна.
        self.setCentralWidget(widget)
        # Добавляет переданный виджет widget  в лейоут(вертикальный-главный)
        main_layout.addWidget(self._view)
        # добавление в виджет гориз лейаута
        main_layout.addLayout(tmp_layout)
        # добавление в гориз виджет кнопок
        tmp_layout.addWidget(self._buttonAdd)
        for button, _ in self._buttons:
            tmp_layout.addWidget(button)
        tmp_layout.addWidget(self._quit)

    def setModel(self, model):
        if model is None:
            return
        self._view.setModel(model)

    def add_to_db(self):
        ui_elements = [("Адрес", QLineEdit()), ("Закупка", QComboBox())]
        ui_elements[1][1].addItems(get_purchases())
        dialog = Dialog(ui_elements, "Добавить запись")
        if dialog.exec() == QDialog.Accepted:
            self._view.setText(add_branch(ui_elements[0][1].text(), ui_elements[1][1].currentText()))

    def query_1(self):

        ui_elements = [("", QLabel(DESCRIPTION_1)), ("Предметы :", QComboBox())]
        ui_elements[1][1].addItems(get_goods())
        dialog = Dialog(ui_elements, "Найти руководителей")

        if dialog.exec() == QDialog.Accepted:
            self._view.setText(query1(ui_elements[1][1].currentText()))
            # time.sleep(100)
            # self.setModel(get_result(ui_elements[1][1].currentText()))

    def query_2(self):
        ui_elements = [("", QLabel(DESCRIPTION_2)),
                       ("Проект", QLineEdit())]
        dialog = Dialog(ui_elements, "Получить реквизиты")
        if dialog.exec() == QDialog.Accepted:
            self._view.setText(query2(ui_elements[1][1].text()))
            # self.setModel(get_result(ui_elements[1][1].text()))


    def query_3(self):
        # Example
        button_1 = QRadioButton("фол")
        button_2 = QRadioButton("шил")
        button_3 = QRadioButton("пил")
        ui_elements = [("", QLabel(DESCRIPTION_3)),
                       ("Бюджет", QSpinBox()),
                       ("", button_1), ("", button_2), ("", button_3)]
        ui_elements[1][1].setMaximum(max_budget())
        dialog = Dialog(ui_elements, "Поиск по названию оборудования")
        if dialog.exec() == QDialog.Accepted:
            val = ui_elements[1][1].value()
            if (button_1.isChecked()):
                self._view.setText(query3(val, 'фол'))
            if (button_2.isChecked()):
                self._view.setText(query3(val, 'шил'))
                # self.setModel(get_result(val, '2'))
            if (button_3.isChecked()):
                self._view.setText(query3(val, 'пил'))

                # self.setModel(get_result(val, '3'))   

