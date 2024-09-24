import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox

class MainWindow(QWidget):
    def __init__(self, csv_file):
        super().__init__()
        self.csv_file = csv_file
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
        """Загружает список игрушек из CSV файла."""
        try:
            toys_df = pd.read_csv(self.csv_file)
            self.toy_list_widget.clear()  # Очищаем список перед загрузкой
            # Добавляем каждую игрушку в виджет списка
            for toy in toys_df['Toy Name']:
                self.toy_list_widget.addItem(toy)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось прочитать файл CSV: {e}")


