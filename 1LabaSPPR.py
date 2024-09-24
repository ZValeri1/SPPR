import sys
import pandas as pd
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QInputDialog, QMessageBox, QPushButton, \
    QMainWindow, QListWidget, QHBoxLayout
import CSV_of_toys
import Questions


class ToyQuestionnaireApp(QMainWindow):
    def __init__(self, csv_file):
        super().__init__()
        self.toy_names = []
        self.csv_file = csv_file
        self.answers = {}
        self.questions = [
            ("Вы ищете игрушку для мальчика или девочки?", ["1 - Мальчик", "2 - Девочка", "3 - На обоих"]),
            ("Хотите, чтобы ваш ребенок больше времени проводил на свежем воздухе?",
             ["1 - Да", "2 - Нет", "3 - Не знаю"]),
            ("Вы хотите, чтобы ребенок научился чему-то новому?", ["1 - Да", "2 - Нет", "3 - Не знаю"]),
            ("Вы хотите, чтобы ваш ребенок больше двигался благодаря этой игрушке?",
             ["1 - Да", "2 - Нет", "3 - Не знаю"]),
            ("Хотели бы вы рассмотреть игрушки с перезаряжаемой батареей / для подключения к розетке?",
             ["1 - Да", "2 - Нет"]),
            ("На сколько человек должна быть рассчитана игра?",
             ["1 - Для одного человека", "2 - Для двух и больше", "3 - Не знаю"]),
            ("Сколько лет вашему ребенку?", ["1 - 0-2", "2 - 3-5", "3 - 6-8", "4 - 9-12", "5 - 13+"]),
            ("Какую максимальную сумму вы готовы потратить?", "Введите число")
        ]
        self.current_question_index = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Настройки опроса")

        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)  # Используем горизонтальный layout

        # Настройка вертикального layout для кнопок
        button_layout = QVBoxLayout()

        # Изменяем фоновый цвет окна
        self.setStyleSheet("background-color: #f0f0f0;")  # Светлый серый фон

        # Настройка кнопки "Начать опрос"
        start_button = QPushButton("Начать опрос")
        start_button.clicked.connect(self.start_survey)
        start_button.setFixedSize(300, 100)  # Устанавливаем размеры кнопки
        start_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 28px; border-radius: 10px;")  # Зеленая кнопка с белым текстом
        button_layout.addWidget(start_button)

        # Настройка кнопки "Список игрушек"
        list_toys_button = QPushButton("Список игрушек")
        list_toys_button.clicked.connect(self.show_toys_list)  # Подключаем метод к кнопке
        list_toys_button.setFixedSize(300, 100)  # Устанавливаем размеры кнопки
        list_toys_button.setStyleSheet(
            "background-color: #2196F3; color: white; font-size: 28px; border-radius: 10px;")  # Синяя кнопка с белым текстом
        button_layout.addWidget(list_toys_button)  # Добавляем кнопку в button_layout

        # Добавление отступов между кнопками
        button_layout.addSpacing(10)

        # Добавление центрального вертикального layout в основной горизонтальный layout
        main_layout.addLayout(button_layout)

        # Добавление изображения в окно
        photo_label = QLabel()
        pixmap = QPixmap('C:/Users/User/Desktop/7 семестр/СППР/toys.png')
        photo_label.setPixmap(pixmap)

        # Зафиксируем размер изображения
        #photo_label.setFixedSize(170, 170)  # Установите желаемые размеры для изображения
        main_layout.addWidget(photo_label, alignment=Qt.AlignRight)  # Добавляем изображение справа

        self.resize(700, 405)  # Размеры окна - увеличьте для лучшего отображения
        self.setFixedSize(700, 405)  # Убедитесь, что окна фиксированы, как вам нужно

    def start_survey(self):
        self.close()
        self.current_question_index = 0
        self.questions = Questions.SurveyWindow('C:/Users/User/Desktop/7 семестр/СППР/toys_database1.csv')
        self.questions.show()

    def show_toys_list(self):
        self.toys_window = CSV_of_toys.MainWindow('C:/Users/User/Desktop/7 семестр/СППР/toys_database1.csv')  # Передаем список игрушек в ваше окно
        self.toys_window.show()  # Показываем новое окно


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToyQuestionnaireApp('C:/Users/User/Desktop/7 семестр/СППР/toys_database1.csv')
    window.show()
    app.exec_()