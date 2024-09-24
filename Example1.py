import List_of_toys
import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QInputDialog, \
    QHBoxLayout, QLineEdit, QComboBox


class SurveyWindow(QWidget):
    def __init__(self, csv_file, parent=None):
        super().__init__(parent)
        self.toy_names = None
        self.show_results = None
        self.questions =  [
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
        self.csv_file = csv_file
        self.current_question_index = 0
        self.answers = {}

        self.initUI()
        self.show_question()

    def initUI(self):
        self.setWindowTitle("Опрос")
        layout = QVBoxLayout()

        self.question_label = QLabel("")
        layout.addWidget(self.question_label)

        self.answer_widget = QWidget()
        self.answer_layout = QHBoxLayout(self.answer_widget)

        self.answer_input = QLineEdit()  # Поле для ввода текста
        self.answer_combo = QComboBox()  # Выпадающий список для выбора
        self.answer_layout.addWidget(self.answer_input)
        self.answer_layout.addWidget(self.answer_combo)
        self.answer_widget.setVisible(False)  # Скрываем пока

        layout.addWidget(self.answer_widget)

        self.prev_button = QPushButton("Назад")
        self.prev_button.clicked.connect(self.show_previous_question)
        layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Далее")
        self.next_button.clicked.connect(self.next_question)
        layout.addWidget(self.next_button)

        self.setLayout(layout)
        self.resize(400, 300)
        self.setFixedSize(400, 300)

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
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл CSV: {e}")
            return

        df = toys_df.copy()

        if self.answers[0] == '1 - Мальчик':
            df = df[df["For Boys"]]
        elif self.answers[0] == '2 - Девочка':
            df = df[df['For Girls']]
        if self.answers[1] == '1 - Да':
            df = df[df['For Outdoor Play']]
        elif self.answers[1] == '2 - Нет':
            df = df[~df['For Outdoor Play']]
        if self.answers[2] == '1 - Да':
            df = df[df['Educational']]
        elif self.answers[2] == '2 - Нет':
            df = df[~df['Educational']]
        if self.answers[3] == '1 - Да':
            df = df[df['Requires Movement']]
        elif self.answers[3] == '2 - Нет':
            df = df[~df['Requires Movement']]
        if self.answers[4] == '2 - Нет':
            df = df[~df['Electronic']]
        if self.answers[5] == '1 - Для одного человека':
            df = df[df['For One Person']]
        elif self.answers[5] == '2 - Для двух и больше':
            df = df[df['Multiplayer']]
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

        max_price = self.answers[7] if self.answers[7].isdigit() else 0
        df = df[df['Price'] <= int(max_price)]

        # Получение названий игрушек
        toy_names = df['Toy Name']
        self.toy_names = toy_names.head(3).values  # Получаем только первые три названия
        print(self.toy_names)
        # Вывод результата
        #self.show_results = List_of_toys.MainWindow(self.toy_names)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SurveyWindow('C:/Users/User/Desktop/7 семестр/СППР/toys_database1.csv')
    window.show()
    sys.exit(app.exec_())