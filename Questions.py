import sys
import List_of_toys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QInputDialog, QMessageBox, QPushButton, \
    QMainWindow, QListWidget, QHBoxLayout, QLineEdit, QComboBox


class SurveyWindow(QWidget):
    def __init__(self, csv_file, parent=None):
        super().__init__(parent)
        self.toy_names = []
        self.questions = [
            ("Вы ищете игрушку для мальчика или девочки?", ["1 - Мальчик", "2 - Девочка", "3 - На обоих"]),
            ("Игрушку для игры на улице?",
             ["1 - Да", "2 - Нет", "3 - Не знаю"]),
            ("Игрушка должна быть познавательной?", ["1 - Да", "2 - Нет", "3 - Не знаю"]),
            ("Игрушка для активного образа жизни?",
             ["1 - Да", "2 - Нет", "3 - Не знаю"]),
            ("Игрушка может быть электрической?",
             ["1 - Да", "2 - Нет"]),
            ("На сколько человек рассчитана игра?",
             ["1 - Для одного человека", "2 - Для двух и больше", "3 - Не знаю"]),
            ("Сколько лет вашему ребенку?", ["1 - 0-2", "2 - 3-5", "3 - 6-8", "4 - 9-12", "5 - 13+"]),
            ("Ваш бюджет:", "Введите число")
        ]
        self.csv_file = csv_file
        self.current_question_index = 0
        self.answers = {}
        self.initUI()
        self.show_question()

    def initUI(self):
        self.setWindowTitle("Опрос")

        # Основной layout будет вертикальным
        layout = QVBoxLayout()

        self.question_label = QLabel("")
        self.question_label.setStyleSheet("font-size: 40px;")  # Увеличиваем текст вопросов
        layout.addWidget(self.question_label)

        self.answer_widget = QWidget()
        self.answer_layout = QHBoxLayout(self.answer_widget)

        self.answer_input = QLineEdit()  # Поле для ввода текста
        self.answer_input.setFixedHeight(40)  # Фиксируем высоту поля ввода
        self.answer_layout.addWidget(self.answer_input)


        self.answer_combo = QComboBox()  # Выпадающий список для выбора
        self.answer_combo.setStyleSheet("font-size: 20px;")
        self.answer_combo.setFixedHeight(40)  # Фиксируем высоту выпадающего списка
        self.answer_layout.addWidget(self.answer_combo)

        self.answer_widget.setVisible(False)  # Скрываем пока
        layout.addWidget(self.answer_widget)

        # Создаем отдельный layout для кнопок внизу
        button_layout = QHBoxLayout()

        self.prev_button = QPushButton("Назад")
        self.prev_button.clicked.connect(self.show_previous_question)
        self.prev_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 28px; border-radius: 20px;")
        button_layout.addWidget(self.prev_button)
        self.prev_button.setFixedSize(100, 50)

        button_layout.addStretch()  # Добавляем растяжение для пробела между кнопками

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_question)
        self.next_button.setStyleSheet(
            "background-color: #4CAF50; color: white; font-size: 28px; border-radius: 20px;")
        button_layout.addWidget(self.next_button)
        self.next_button.setFixedSize(100, 50)

        # Добавляем кнопки в основной layout
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.resize(900, 300)
        self.setFixedSize(900, 300)

    def show_question(self):
        """Отображает текущий вопрос и варианты ответов."""
        question_text, options = self.questions[self.current_question_index]
        self.question_label.setText(question_text)

        # Проверка, являются ли ответы списком или текстом
        if isinstance(options, list):
            self.answer_widget.setVisible(True)
            self.answer_combo.clear()
            self.answer_input.setVisible(False)
            self.answer_combo.addItems(options)
        else:
            self.answer_widget.setVisible(True)
            self.answer_input.setText("")
            self.answer_input.setVisible(True)
            self.answer_combo.clear()
            self.answer_combo.setVisible(False)

    def next_question(self):
        """Переходит к следующему вопросу."""
        if self.current_question_index < len(self.questions) - 1:
            # Сохраняем ответ
            if self.answer_combo.isVisible():
                answer = self.answer_combo.currentText()
                self.answers[self.current_question_index] = answer
            else:
                answer = self.answer_input.text()
                self.answers[self.current_question_index] = answer

            self.current_question_index += 1
            self.show_question()
        else:
            self.finish_survey()

    def show_previous_question(self):
        """Возвращается к предыдущему вопросу."""
        if self.current_question_index > 0:
            # Сохраняем ответ
            if self.answer_combo.isVisible():
                answer = self.answer_combo.currentText()
                self.answers[self.current_question_index] = answer
            else:
                answer = self.answer_input.text()
                self.answers[self.current_question_index] = answer

            self.current_question_index -= 1
            self.show_question()

    def finish_survey(self):
        """Заканчивает опрос и обрабатывает результаты."""
        self.filter_toys()

    def filter_toys(self):
        try:
            toys_df = pd.read_csv(self.csv_file)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to read CSV file: {e}")
            return
        df = toys_df.copy()
        print("Исходные данные:\n", df)
        # Пример фильтрации базируясь на ответах
        print("Ответы пользователя:\n", self.answers)

        if self.answers[0] == '1 - Мальчик':
            df = df[df["For Boys"]]
        elif self.answers[0] == '2 - Девочка':
            df = df[df['For Girls']]
        print("После фильтрации по мальчикам/девочкам:\n", df)
        if self.answers[1] == '1 - Да':
            df = df[df['For Outdoor Play']]
        elif self.answers[1] == '2 - Нет':
            df = df[~df['For Outdoor Play']]
        print("После фильтрации по игре на свежем воздухе:\n", df)
        if self.answers[2] == '1 - Да':
            df = df[df['Educational']]
        elif self.answers[2] == '2 - Нет':
            df = df[~df['Educational']]
        print("После фильтрации по познавательности:\n", df)
        if self.answers[3] == '1 - Да':
            df = df[df['Requires Movement']]
        elif self.answers[3] == '2 - Нет':
            df = df[~df['Requires Movement']]
        print("После фильтрации по движению:\n", df)
        if self.answers[4] == '2 - Нет':
            df = df[~df['Electronic']]
        print("После фильтрации по электрике:\n", df)
        if self.answers[5] == '1 - Для одного человека':
            df = df[df['For One Person']]
        elif self.answers[5] == '2 - Для двух и больше':
            df = df[df['Multiplayer']]
        print("После фильтрации по одиночной или игре в компании:\n", df)
        if self.answers[6] == '1 - 0-2':
            df = df[df['Age Range 0-2']]
        elif self.answers[6] == '2 - 3-5':
            df = df[df['Age Range 3-5']]
        elif self.answers[6] == '3 - 6-8':
            df = df[df['Age Range 6-8']]
        elif self.answers[6] == '4 - 9-12':
            df = df[df['Age Range 9-12']]
        elif self.answers[6] == '5 - 13+':
            df = df[df['Age Range 13+']]
        print("После фильтрации по возрасту:\n", df)
        #max_price = self.answers[7]
        #if max_price.isdigit():
            #df = df[df['Price'] <= int(max_price)]
            # Получение названий игрушек
        toy_names = df['Toy Name']
        self.toy_names = toy_names.head(3).values  # Получаем только первые три названия
        self.toy_names = toy_names.tolist()
        self.toy_names_final = [self.toy_names[0], self.toy_names[1], self.toy_names[2]]
        print("Выборка товаров для пользователя:\n", self.toy_names_final)  # Выводим подходящие игрушки

        self.results_window = List_of_toys.MainWindow(self.toy_names_final)
        self.results_window.show()


