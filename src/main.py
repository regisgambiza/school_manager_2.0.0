# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.app.school_manager import Ui_MainWindow


class SchoolManagerApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # This sets up the UI from the generated file


def main():
    app = QApplication(sys.argv)
    school_manager_app = SchoolManagerApp()
    school_manager_app.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
