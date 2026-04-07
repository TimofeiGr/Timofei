import sys
import random
import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QMessageBox, QFrame, QShortcut)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QKeySequence

# --- КОНСТАНТЫ И ДАННЫЕ ---
DICE_FACES = {
    1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"
}


class DiceModel:
    """Логика приложения (Model)"""

    def roll(self):
        return random.randint(1, 6)


class DiceApp(QMainWindow):
    """Основное окно приложения (View + Controller)"""

    def __init__(self):
        super().__init__()
        self.model = DiceModel()
        self.history_file = "dice_history.txt"
        self.init_ui()
        self.setup_shortcuts()

    def init_ui(self):
        """Инициализация графического интерфейса"""
        self.setWindowTitle("Симулятор Кубика")
        self.setMinimumSize(400, 500)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 1. Область отображения кубика
        self.dice_label = QLabel("⚀")
        self.dice_label.setAlignment(Qt.AlignCenter)
        self.dice_label.setFont(QFont("Segoe UI Symbol", 150))
        self.dice_label.setStyleSheet("color: #ffffff;")

        dice_frame = QFrame()
        dice_frame.setFrameStyle(QFrame.Box | QFrame.Sunken)
        dice_frame.setStyleSheet("background-color: #2c3e50; border-radius: 15px;")
        frame_layout = QVBoxLayout(dice_frame)
        frame_layout.addWidget(self.dice_label)

        # 2. Кнопка действия
        self.roll_button = QPushButton("Бросить кубик")
        self.roll_button.setFixedSize(200, 60)
        self.roll_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.roll_button.setCursor(Qt.PointingHandCursor)
        self.roll_button.clicked.connect(self.handle_roll)

        # 3. Лог событий
        history_label = QLabel("История бросков:")
        history_label.setStyleSheet("color: #bdc3c7; font-weight: bold;")

        self.history_log = QTextEdit()
        self.history_log.setReadOnly(True)
        self.history_log.setMaximumHeight(100)
        self.history_log.setStyleSheet("""
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                border: 1px solid #7f8c8d;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Сборка интерфейса
        main_layout.addWidget(dice_frame, stretch=2)
        main_layout.addWidget(self.roll_button, alignment=Qt.AlignCenter)
        main_layout.addWidget(history_label)
        main_layout.addWidget(self.history_log, stretch=1)

        self.apply_styles()

    def apply_styles(self):
        """Применение темной темы оформления"""
        self.setStyleSheet("""
            QMainWindow { background-color: #8B0000; }
            QPushButton {
                background-color: #e74c3c; color: white;
                border: none; border-radius: 10px;
            }
            QPushButton:hover { background-color: #c0392b; }
            QPushButton:pressed { background-color: #96281b; }
        """)

    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        shortcut = QShortcut(QKeySequence("Space"), self)
        shortcut.activated.connect(self.handle_roll)
        shortcut_enter = QShortcut(QKeySequence("Return"), self)
        shortcut_enter.activated.connect(self.handle_roll)

    def handle_roll(self):
        """Обработка события броска"""
        try:
            result = self.model.roll()
            self.dice_label.setText(DICE_FACES[result])

            # Визуальный отклик
            self.dice_label.setStyleSheet("color: #f1c40f;")
            QApplication.processEvents()
            self.dice_label.setStyleSheet("color: #ffffff;")

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] Выпало: {result}\n"

            self.history_log.insertPlainText(log_entry)
            self.history_log.verticalScrollBar().setValue(
                self.history_log.verticalScrollBar().maximum()
            )

            self.save_to_file(log_entry)

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла критическая ошибка: {str(e)}")

    def save_to_file(self, text):
        """Обработка исключений при работе с файлами"""
        try:
            with open(self.history_file, "a", encoding="utf-8") as f:
                f.write(text)
        except PermissionError:
            self.history_log.insertPlainText("--- ОШИБКА: Нет прав на запись ---\n")
        except IOError:
            self.history_log.insertPlainText("--- ОШИБКА: Не удалось записать в файл ---\n")

    def keyPressEvent(self, event):
        """Перехват событий клавиатуры"""
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    window = DiceApp()
    window.show()
    sys.exit(app.exec_())
