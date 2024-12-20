import sys
from src.application.Application import MainApp
from PySide6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
