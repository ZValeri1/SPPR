import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QInputDialog, QMessageBox, QPushButton


class ToyQuestionnaireApp(QWidget):
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
        layout = QVBoxLayout()

        start_button = QPushButton("Начать опрос")
        start_button.clicked.connect(self.start_survey)
        layout.addWidget(start_button)

        self.setLayout(layout)
        self.resize(300, 200)  # Размер начального окна
        self.setFixedSize(300, 200)  # Зафиксировать размер окна

    def start_survey(self):
        self.close()
        self.current_question_index = 0
        self.ask_question(self.current_question_index)
    def ask_question(self, index):
        if index < len(self.questions):
            question_text, options = self.questions[index]
            answer = None
            if isinstance(options, list):
                answer, ok = QInputDialog.getItem(self, "Question", question_text, options, 0, False)
            else:
                answer, ok = QInputDialog.getText(self, "Question", question_text)

            if ok and answer:
                self.answers[index] = answer
                self.current_question_index += 1
                self.ask_question(self.current_question_index)
            else:
                QMessageBox.warning(self, 'Input Error', 'Please provide an answer.')
                self.ask_question(index)
        else:
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
        max_price = self.answers[7]
        if max_price.isdigit():
            df = df[df['Price'] <= int(max_price)]

            # Получение названий игрушек
            toy_names = df['Toy Name']
            self.toy_names = toy_names.head(3).values  # Получаем только первые три названия
            print("Выборка товаров для пользователя:\n", self.toy_names)  # Выводим подходящие игрушки


    def show_results(self, toy_names_array):
        results_window = QWidget()
        results_window.setWindowTitle("Подходящие игрушки")
        layout = QVBoxLayout()

        if len(toy_names_array) > 0:  # Если есть игрушки
            results_text = "\n".join(toy_names_array)  # Соединяем элементы массива в строку
        else:
            results_text = "Не найдено подходящих игрушек."

        label = QLabel(results_text)
        layout.addWidget(label)

        close_button = QPushButton("Закрыть")
        close_button.clicked.connect(results_window.close)
        layout.addWidget(close_button)

        results_window.setLayout(layout)
        results_window.resize(300, 200)  # Установка размеров окна
        results_window.move(400, 300)  # Установка положения окна на экране
        results_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToyQuestionnaireApp('C:/Users/User/Desktop/7 семестр/СППР/toys_database1.csv')
    window.show()
    sys.exit(app.exec_())
