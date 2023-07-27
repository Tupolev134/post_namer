import os
import re
import subprocess
from datetime import date
import os
import shutil

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QProgressBar, \
    QComboBox, QLineEdit, QFileDialog, QMessageBox, QFrame, QHBoxLayout, QGridLayout, QScrollArea
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

from core.data.EmailTemplate import EmailTemplate
from core.data.Profile import Profile


def _get_line_widget():
    line = QFrame()
    line.setFrameShape(QFrame.Shape.HLine)
    line.setFrameShadow(QFrame.Shadow.Sunken)
    return line

class MainMenu(QMainWindow):
    switch_requested = pyqtSignal(Profile)

    def __init__(self):
        super().__init__()
        self.profile = Profile.load_from_json(r"C:/Users/TheOverlanders/Desktop/Coding/post_namer/test_data/profile_OL_win.json")
        self.template = EmailTemplate.load_from_json(r"C:/Users/TheOverlanders/Desktop/Coding/post_namer/test_data/template.json")

        # Sections
        self.heading_section_layout = None
        self.profile_section_layout = None
        self.email_section_layout = None
        self.starting_section_layout = None

        # ----------- Heading Section
        self.heading_label = QLabel("PDF namer by Tupolev134")
        # ----------- Profile Section
        # 0
        self.profile_label = QLabel("No Profile loaded")
        self.profile_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.load_profile_btn = QPushButton("Load a Profile", self)
        # 1
        self.path_label = QLabel("No Path loaded")
        self.path_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        # 2
        self.recipients_label = QLabel("No recipients loaded")
        self.recipients_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.edit_recipients_list_btn = QPushButton("Edit Recipients", self)
        # 3
        self.populate_stats_label = QLabel("No Populated Profile Loaded")
        self.populate_stats_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.populate_profile_btn = QPushButton("Populate current Profile", self)
        # ----------- Email Section
        self.email_expand_btn = QPushButton("Show Emailer", self)

        self.template_label = QLabel("No Email Template Loaded")
        self.template_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.load_email_template_btn = QPushButton("Load a Email Template", self)
        self.sender_label = QLabel("No sender address in Template")
        self.sender_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.add_sender = QPushButton("Add a sender")
        self.to_label = QLabel("No recipients in Template")
        self.to_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.add_recipients = QPushButton("Add a new recipient")
        self.cc_label = QLabel("No cc recipients in Template")
        self.cc_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.add_cc = QPushButton("Add a new cc recipient")
        self.bcc_label = QLabel("No bcc recipient loaded")
        self.bcc_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.add_bcc_btn = QPushButton("Add a new bcc recipient")
        self.subject_label = QLabel("No subject loaded")
        self.subject_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.add_subject_label = QPushButton("Add or edit the subject")
        self.body_label = QLabel("No body loaded")
        self.body_label.setStyleSheet("background-color: grey; border-radius: 10px; padding: 6px;")
        self.add_body_btn = QPushButton("Add or edit body")
        self.attachment_label = QLabel("No attachment folder loaded")
        self.add_attachment_btn = QPushButton("Add or edit attachment folder")
        # ----------- Start Section
        self.start_btn = QPushButton("Start Naming", self)
        self.email_btn = QPushButton("Generate Email", self)
        # ----------- Main Window
        self.setWindowTitle("PDF Renamer")
        self.resize(1300, 500)
        # Create central widget
        # Create a QScrollArea and set its widget to the content_widget
        central_widget = QWidget()
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)

        # Set the QMainWindow's central widget to the QScrollArea
        self.setCentralWidget(scroll_area)

        # Get the screen size and set the maximum height of the window
        screen = QApplication.primaryScreen()
        rect = screen.availableGeometry()
        self.setMaximumHeight(rect.height())

        # Create central widget
        self.setCentralWidget(scroll_area)
        self.main_layout = QVBoxLayout(central_widget)

        self.create_heading_section()
        self.create_profile_section()
        self.create_email_section()
        self.create_starting_section()

        self.main_layout.addLayout(self.heading_section_layout)
        self.main_layout.addWidget(_get_line_widget())
        self.main_layout.addLayout(self.profile_section_layout)
        self.main_layout.addWidget(_get_line_widget())
        self.main_layout.addLayout(self.email_section_layout)
        self.main_layout.addWidget(_get_line_widget())
        self.main_layout.addLayout(self.starting_section_layout)
        self.update_profile_info()
        self.update_template_info()

    def create_heading_section(self):
        self.heading_section_layout = QHBoxLayout()
        self.heading_section_layout.addStretch()
        self.heading_section_layout.addWidget(self.heading_label)
        self.heading_section_layout.addStretch()

    def create_profile_section(self):
        self.profile_section_layout = QGridLayout()
        self.profile_section_layout.addWidget(self.profile_label, 0, 0)
        self.profile_section_layout.addWidget(self.load_profile_btn, 0, 1)
        self.profile_section_layout.addWidget(self.path_label, 1, 0)
        self.profile_section_layout.addWidget(self.recipients_label, 2, 0)
        self.profile_section_layout.addWidget(self.edit_recipients_list_btn, 2, 1)
        self.profile_section_layout.addWidget(self.populate_stats_label, 3, 0)
        self.profile_section_layout.addWidget(self.populate_profile_btn, 3, 1)

        self.populate_profile_btn.clicked.connect(self.populate_pdf_files)
        self.load_profile_btn.clicked.connect(self.load_profile)

    def create_email_section(self):
        self.email_section_layout = QGridLayout()
        self.email_section_layout.addWidget(self.email_expand_btn, 0, 0)
        self.email_expand_btn.clicked.connect(self.expand_email_section)

    def expand_email_section(self):
        self.email_section_layout = QGridLayout()
        self.email_section_layout.addWidget(self.template_label, 0, 0)
        self.email_section_layout.addWidget(self.load_email_template_btn, 0, 1)
        self.email_section_layout.addWidget(self.sender_label, 1, 0)
        self.email_section_layout.addWidget(self.add_sender, 1, 1)
        self.email_section_layout.addWidget(self.to_label, 2, 0)
        self.email_section_layout.addWidget(self.add_recipients, 2, 1)
        self.email_section_layout.addWidget(self.cc_label, 3, 0)
        self.email_section_layout.addWidget(self.add_cc, 3, 1)
        self.email_section_layout.addWidget(self.bcc_label, 4, 0)
        self.email_section_layout.addWidget(self.add_bcc_btn, 4, 1)
        self.email_section_layout.addWidget(self.subject_label, 5, 0)
        self.email_section_layout.addWidget(self.add_subject_label, 5, 1)
        self.email_section_layout.addWidget(self.body_label, 6, 0)
        self.email_section_layout.addWidget(self.add_body_btn, 6, 1)
        self.email_section_layout.addWidget(self.attachment_label, 7, 0)
        self.email_section_layout.addWidget(self.add_attachment_btn, 7, 1)
        self.load_email_template_btn.clicked.connect(self.load_templates)

        # self.configure_a_profile = QPushButton("Configure a new Profile", self)
        # self.configure_existing_profile = QPushButton("Configure an existing Profile", self)
        # self.main_layout.addWidget(self.configure_a_profile)
        # self.main_layout.addWidget(self.configure_existing_profile)

        # self.loading_section_layout.addWidget(_get_line_widget())
        self.main_layout.addLayout(self.email_section_layout)

    def create_starting_section(self):
        self.starting_section_layout = QVBoxLayout()
        self.starting_section_layout.addWidget(self.start_btn)
        self.starting_section_layout.addWidget(self.email_btn)
        self.start_btn.clicked.connect(self.switch_to_pdf_renamer)
        self.email_btn.clicked.connect(self.generate_apple_mail)

    # -------------------- Utils --------------------

    def populate_pdf_files(self):
        num_files_viewed = 0
        num_split_err = 0
        num_date_err = 0
        self.profile.origins = []
        self.profile.references = []
        self.profile.identifications = []

        file_dialog = QFileDialog()
        populate_path = file_dialog.getExistingDirectory()
        for root, dirs, files in os.walk(populate_path):
            for file in files:
                if file.endswith('.pdf'):
                    num_files_viewed += 1
                    file = file.strip(".pdf")
                    parts = file.split(" - ")
                    if len(parts) < 5:
                        # print(f"Split error: {file}")
                        num_split_err += 1
                        break
                    # The first part is the recipient
                    # self.profile.add_recipient(parts[0])

                    # The second part is the origin
                    self.profile.add_origin(parts[1])

                    # The third part is the reference
                    self.profile.add_reference(parts[2])

                    # The last part is the date. We check it with a simple regex to confirm.
                    date_pattern = re.compile("\d{2}.\d{2}.\d{4}$")
                    if date_pattern.match(parts[-1]): self.date = parts[-1]
                    else:
                        # print(f"Date error: {file}")
                        num_date_err += 1
                        break

                    # Everything else is part of the identification
                    self.profile.add_identification(" - ".join(parts[3:-1]))
        self.profile.save_to_json(self.profile.path_to_this_profile)
        print(f"files viewed: {num_files_viewed}")
        print(f"split errors: {num_split_err}")
        print(f"date errors: {num_date_err}")
        self.update_profile_info()

    def load_profile(self):
        file_dialog = QFileDialog()
        json_filter = "JSON (*.json)"
        profile_file_path, _ = file_dialog.getOpenFileName(filter=json_filter)
        if profile_file_path:
            try:
                self.profile = Profile.load_from_json(profile_file_path)
                self.update_profile_info()
            except Exception as e:
                # Log the exception and optionally show a user-friendly error message.
                print(f"Error loading profile: {e}")
                # Here you might want to show a user-friendly error message to the user,
                # for example using a QMessageBox.
                QMessageBox.critical(self, "Error", "Could not load profile.")

    def load_templates(self):
        file_dialog = QFileDialog()
        json_filter = "JSON (*.json)"
        templates_file_path, _ = file_dialog.getOpenFileName(filter=json_filter)
        if templates_file_path:
            try:
                self.template = EmailTemplate.load_from_json(templates_file_path)
                self.update_profile_info()
                self.template.subject = self.template.subject + date.today().strftime("%d.%m.%Y")
            except Exception as e:
                # Log the exception and optionally show a user-friendly error message.
                print(f"Error loading profile: {e}")
                # Here you might want to show a user-friendly error message to the user,
                # for example using a QMessageBox.
                QMessageBox.critical(self, "Error", "Could not load profile.")

    def update_profile_info(self):
        self.profile_label.setText(f"Profile: \n{self.profile.name}")
        self.path_label.setText(f"Root Path: {self.profile.path_to_root} \nScan Path: {self.profile.path_to_scans}")
        self.recipients_label.setText(f"Recipients: \n{', '.join(self.profile.recipients)}")
        self.populate_stats_label.setText(f"Population Status: \nOrigins: {len(self.profile.origins)} \nReferences: {len(self.profile.references)} \nIdentifications: {len(self.profile.identifications)}")

    def update_template_info(self):
        self.template_label.setText(f"Email Template: \n{self.template.template_name}")

        self.sender_label.setText(f"Sender: \n{self.template.sender}")

        to_text = ', '.join(self.template.to) if self.template.to else 'None'
        self.to_label.setText(f"TO: \n{to_text}")

        cc_text = ', '.join(self.template.cc) if self.template.cc else 'None'
        self.cc_label.setText(f"CC: \n{cc_text}")

        bcc_text = ', '.join(self.template.bcc) if self.template.bcc else 'None'
        self.bcc_label.setText(f"BCC: \n{bcc_text}")

        subject_text = self.template.subject if self.template.subject else 'None'
        self.subject_label.setText(f"Subject: \n{subject_text}")

        body_text = self.template.body if self.template.body else 'None'
        self.body_label.setText(f"{body_text}")

    def generate_apple_mail(self):
        # Check if attachments exist
        attachment_string = ""
        if self.template.attachments:
            attachment_string = "".join(
                f'add attachment at after last paragraph {path}' for path in self.template.attachments)

        # AppleScript command to create a new mail with details from email template
        applescript_command = f"""
        tell application "Mail"
            set newMessage to make new outgoing message with properties {{subject: "{self.template.subject}", content: "{self.template.body}", sender: "{self.template.sender}"}}
            tell newMessage
                make new to recipient at end of to recipients with properties {{address: "{', '.join(self.template.to)}"}}
                make new cc recipient at end of cc recipients with properties {{address: "{', '.join(self.template.cc)}"}}
                make new bcc recipient at end of bcc recipients with properties {{address: "{', '.join(self.template.bcc)}"}}
                {attachment_string}
            end tell
            activate
        end tell
        """

        # Run the AppleScript command
        subprocess.run(["osascript", "-e", applescript_command])

    def switch_to_pdf_renamer(self):
        self.switch_requested.emit(self.profile)