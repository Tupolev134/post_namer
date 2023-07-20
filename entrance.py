import sys

from PyQt6.QtWidgets import QApplication

from core.UI.MainMenu import MainMenu
from core.UI.PDFRenamer import PDFRenamer


class ApplicationWindowManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.current_window = None

    def start(self):
        self.show_main_menu()
        sys.exit(self.app.exec())

    def show_main_menu(self):
        if self.current_window is not None:
            self.current_window.close()

        self.current_window = MainMenu()
        self.current_window.switch_requested.connect(self.show_pdf_renamer)
        self.current_window.show()

    def show_pdf_renamer(self, profile):
        if self.current_window is not None:
            self.current_window.close()

        self.current_window = PDFRenamer(profile)
        self.current_window.switch_requested.connect(self.show_main_menu)
        self.current_window.show()

if __name__ == '__main__':
    manager = ApplicationWindowManager()
    manager.start()