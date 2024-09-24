import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox

class MainWindow(QWidget):
    def __init__(self, toys_list):
        super().__init__()
        self.toys_list = toys_list  # Сохраняем переданный список
        self.initUI()
        self.load_toys()

    def initUI(self):
        self.setWindowTitle("Список игрушек")
        layout = QVBoxLayout()

        self.toy_list_widget = QListWidget()  # Создаем виджет списка
        layout.addWidget(self.toy_list_widget)

        self.setLayout(layout)
        self.resize(400, 300)
        self.setFixedSize(400, 300)

    def load_toys(self):
        """Загружает список игрушек из переданного списка."""
        self.toy_list_widget.clear()  # Очищаем список перед загрузкой
        try:
            # Если список игрушек пустой, выдать сообщение
            if not self.toys_list:
                raise ValueError("Список игрушек пуст.")

            # Добавляем каждую игрушку в виджет списка
            for toy in self.toys_list:
                self.toy_list_widget.addItem(toy)
                self.toy_list_widget.setStyleSheet("font-size: 20px;")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))
