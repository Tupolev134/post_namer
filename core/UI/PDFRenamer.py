import os
import shutil
import subprocess
import time

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QProgressBar, \
    QComboBox, QLineEdit, QFileDialog, QHBoxLayout, QFrame, QGridLayout, QCompleter, QDateEdit
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal, QStringListModel, QDate

from core.NamingController import NamingController


def clean_file_name(file_name):
    invalid_chars = '\/:*?"<>|'
    for char in invalid_chars:
        file_name = file_name.replace(char, '_')
    return file_name

def _get_line_widget():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line


def get_sorted_list(list_of_tuples):
    return [item[0] for item in sorted(list_of_tuples, key=lambda x: x[1], reverse=True)]


class CustomQDateEdit(QDateEdit):
    enter_pressed = pyqtSignal()  # create a custom signal

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Return:
            self.enter_pressed.emit()


class PDFRenamer(QMainWindow):
    switch_requested = pyqtSignal()

    def __init__(self, profile):
        self.naming_profile = profile
        self.naming_controller = NamingController(profile.path_to_scans)

        super().__init__()
        self.setWindowTitle("PDF Renamer")
        self.resize(450, 600)

        # Navigation
        self.navigation_section_layout = QVBoxLayout()
        self.profile_name_label = QLabel(self.naming_profile.name, self)
        self.close_preview_button = QPushButton("Close Preview Windows", self)
        self.open_current_preview_button = QPushButton("Open Current PDF", self)
        self.main_menu_button = QPushButton("Main Menu", self)
        self.prev_button = QPushButton("Previous", self)
        self.next_button = QPushButton("Next", self)
        self.navigation_label = QLabel(f"{len(self.naming_controller.files)} Files to name", self)
        self.progress = QProgressBar(self)
        self.progress.setRange(0, len(self.naming_controller.files))

        # Naming
        self.naming_section_layout = QGridLayout()

        self.recipient_label = QLabel("recipient:")
        self.recipient_display_label = QLabel("")
        self.recipient_input = QLineEdit()
        recipients_list_model = QStringListModel(self.naming_profile.recipients, self)
        recipients_completer = QCompleter()
        recipients_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        recipients_completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        recipients_completer.setModel(recipients_list_model)
        self.recipient_input.setCompleter(recipients_completer)

        self.origin_label = QLabel("origin:")
        self.origin_display_label = QLabel("")
        self.origin_input = QLineEdit()
        origins_list = get_sorted_list(self.naming_profile.origins)
        origins_list_model = QStringListModel(origins_list, self)
        origins_completer = QCompleter()
        origins_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        origins_completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        origins_completer.setModel(origins_list_model)
        self.origin_input.setCompleter(origins_completer)

        self.reference_label = QLabel("reference:")
        self.reference_display_label = QLabel("")
        self.reference_input = QLineEdit()
        references_list = get_sorted_list(self.naming_profile.references)
        references_list_model = QStringListModel(references_list, self)
        references_completer = QCompleter()
        references_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        references_completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        references_completer.setModel(references_list_model)
        self.reference_input.setCompleter(references_completer)

        self.identification_label = QLabel("identification:")
        self.identification_display_label = QLabel("")
        self.identification_input = QLineEdit()
        identifications_list = get_sorted_list(self.naming_profile.identifications)
        identifications_list_model = QStringListModel(identifications_list, self)
        identifications_completer = QCompleter()
        identifications_completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        identifications_completer.setCompletionMode(QCompleter.CompletionMode.InlineCompletion)
        identifications_completer.setModel(identifications_list_model)
        self.identification_input.setCompleter(identifications_completer)

        self.date_label = QLabel("date:")
        self.date_display_label = QLabel("")
        self.date_input = CustomQDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setDisplayFormat("dd.MM.yyyy")

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        self.create_menu()
        self.create_navigation_section()
        self.create_naming_section()

        self.main_layout.addLayout(self.navigation_section_layout)
        self.main_layout.addLayout(self.naming_section_layout)
        self.main_layout.addWidget(_get_line_widget())

        # os.startfile(self.naming_profile.path_to_scans + "/" + self.naming_controller.current_file.file_name)

        self.update_labels()
        self.recipient_input.setFocus()
        self.raise_()

    # ------------------ Sections ------------------
    def create_navigation_section(self):
        self.navigation_section_layout.addWidget(self.profile_name_label)
        self.navigation_section_layout.addWidget(self.main_menu_button)
        self.navigation_section_layout.addWidget(self.prev_button)
        self.navigation_section_layout.addWidget(self.next_button)
        self.navigation_section_layout.addWidget(self.open_current_preview_button)
        self.navigation_section_layout.addWidget(self.close_preview_button)
        self.navigation_section_layout.addWidget(self.navigation_label)
        self.navigation_section_layout.addWidget(self.progress)
        self.next_button.setAutoDefault(True)
        self.main_menu_button.clicked.connect(self.switch_back_to_main_menu)
        self.next_button.clicked.connect(self.next_file)
        # self.close_preview_button.clicked.connect(lambda: subprocess.run(["osascript", "-e", 'quit app "Preview"']))
        self.open_current_preview_button.clicked.connect(lambda: os.startfile(self.naming_profile.path_to_scans + "/" + self.naming_controller.current_file.file_name))

    def create_naming_section(self):
        self.naming_section_layout.addWidget(self.recipient_label, 0, 0)
        self.naming_section_layout.addWidget(self.recipient_display_label, 0, 1)
        self.naming_section_layout.addWidget(self.recipient_input, 0, 2)
        self.recipient_input.returnPressed.connect(self.origin_input.setFocus)
        self.naming_section_layout.addWidget(self.origin_label, 1, 0)
        self.naming_section_layout.addWidget(self.origin_display_label, 1, 1)
        self.naming_section_layout.addWidget(self.origin_input, 1, 2)
        self.origin_input.returnPressed.connect(self.reference_input.setFocus)
        self.naming_section_layout.addWidget(self.reference_label, 2, 0)
        self.naming_section_layout.addWidget(self.recipient_display_label, 2, 1)
        self.naming_section_layout.addWidget(self.reference_input, 2, 2)
        self.reference_input.returnPressed.connect(self.identification_input.setFocus)
        self.naming_section_layout.addWidget(self.identification_label, 3, 0)
        self.naming_section_layout.addWidget(self.identification_display_label, 3, 1)
        self.naming_section_layout.addWidget(self.identification_input, 3, 2)
        self.identification_input.returnPressed.connect(self.date_input.setFocus)
        self.naming_section_layout.addWidget(self.date_label, 4, 0)
        self.naming_section_layout.addWidget(self.date_display_label, 4, 1)
        self.naming_section_layout.addWidget(self.date_input, 4, 2)
        self.date_input.enter_pressed.connect(self.next_button.setFocus)

    # ------------------ Menu ------------------
    def create_menu(self):
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")

        open_folder_action = QAction("Open Folder", self)
        open_folder_action.triggered.connect(self.open_folder)
        self.file_menu.addAction(open_folder_action)

    # ------------------ File UTILS ------------------

    def next_file(self):
        if self.recipient_input.text() == "" and self.origin_input.text() == "" and self.reference_input.text() == "" \
                and self.identification_input.text() == "":
            pass
        else:
            self.update_file_name()
        self.naming_controller.load_next_file()
        file_path = os.path.join(self.naming_profile.path_to_scans, self.naming_controller.current_file.file_name)
        os.startfile(file_path)
        self.update_labels()
        self.progress.setValue(self.naming_controller.index_current_file)
        self.raise_()
        self.recipient_input.setFocus()

    def update_file_name(self):
        new_file_name = self.recipient_input.text() + " - " + self.origin_input.text() + " - " + self.reference_input.text() + " - " + self.identification_input.text().replace(
            '/', ':') + " - " + self.date_input.text() + ".pdf"
        new_file_name = clean_file_name(new_file_name)
        self.rename_file(self.naming_profile.path_to_scans + "/" + self.naming_controller.current_file.file_name,
                         new_file_name)

    def rename_file(self, file_path, new_name):
        # get the directory of the file
        dir_name = os.path.dirname(file_path)
        # combine the directory with the new name
        new_file_path = os.path.join(dir_name, new_name)
        # rename the file
        os.rename(file_path, new_file_path)

    def update_labels(self):
        self.recipient_display_label.setText(self.naming_controller.current_file.recipient)
        self.origin_display_label.setText(self.naming_controller.current_file.origin)
        self.reference_display_label.setText(self.naming_controller.current_file.reference)
        self.identification_display_label.setText(self.naming_controller.current_file.identification)
        self.date_display_label.setText(self.naming_controller.current_file.date)

        self.recipient_input.setText("")
        self.origin_input.setText("")
        self.reference_input.setText("")
        self.identification_input.setText("")

    # ------------------ GUI UTILS ------------------
    def open_folder(self):
        QFileDialog.getExistingDirectory(self, "Open a folder")

    def switch_back_to_main_menu(self):
        # subprocess.run(["osascript", "-e", 'quit app "Preview"'])
        self.switch_requested.emit()

if __name__ == '__main__':
    PDFRenamer()