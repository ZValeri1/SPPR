
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QInputDialog


class SurveyWindow(QWidget):
    def __init__(self, questions, parent=None):
        super().__init__(parent)
        self.questions = questions
        self.current_question_index = 0
        self.answers = {}

        self.initUI()
        self.show_question()

    def initUI(self):
        self.setWindowTitle("Опрос")
        layout = QVBoxLayout()

        self.question_label = QLabel("")
        layout.addWidget(self.question_label)

        self.answer_buttons = []
        self.buttons_layout = QVBoxLayout()

        # Создание кнопок или текстового поля для ответов
        self.answer_input = QPushButton("")
        self.answer_input.setEnabled(False)
        self.buttons_layout.addWidget(self.answer_input)

        layout.addLayout(self.buttons_layout)

        self.prev_button = QPushButton("Назад")
        self.prev_button.clicked.connect(self.show_previous_question)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.show_next_question)
        layout.addWidget(self.next_button)

        self.setLayout(layout)
        self.resize(300, 200)  # Установка размера окна
        self.setFixedSize(300, 200)  # Зафиксировать размер окна

    def show_question(self):
        """Отображает текущий вопрос и варианты ответов."""
        question_text, options = self.questions[self.current_question_index]
        self.question_label.setText(question_text)

        if isinstance(options, list):
            self.answer_input.setEnabled(True)
            self.answer_input.setText("Выберите вариант")
            self.answer_input.clicked.connect(lambda: self.select_answer(options))
        else:
            self.answer_input.setEnabled(True)
            self.answer_input.setText("Введите ответ")
            self.answer_input.clicked.connect(lambda: self.input_answer())

    def select_answer(self, options):
        """Обработчик, который позволяет выбрать ответ из вариантов."""
        answer, ok = QInputDialog.getItem(self, "Вопрос", self.question_label.text(), options, 0, False)
        if ok and answer:
            self.answers[self.current_question_index] = answer
            self.next_question()

    def input_answer(self):
        """Обработка ввода ответа пользователем."""
        # Здесь можно добавить QInputDialog для ввода текста, например
        # and handle it like above showing a new QInputDialog
        self.answers[self.current_question_index] = "User input"  # Замените это на ввод пользователя
        self.next_question()

    def next_question(self):
        """Переходит к следующему вопросу."""
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.show_question()
        else:
            self.finish_survey()

    def show_previous_question(self):
        """Возвращается к предыдущему вопросу."""
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def finish_survey(self):
        """Заканчивает опрос и обрабатывает результаты."""
        # Здесь можно обработать результаты опроса
        QMessageBox.information(self, "Опрос завершён", "Спасибо за участие!")
        self.close()