import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QFrame, QMessageBox, QStyle)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon, QAction
from back_end import functions as functions
from back_end import classes as classes 
from login import LoginWindow

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Car Rental - Register")

        # 1. ΦΟΝΤΟ (BACKGROUND)
        self.bg_label = QLabel(self)
        self.bg_label.lower() 
        self.original_pixmap = QPixmap('assets/bg.jpg')

        # ΚΥΡΙΟ LAYOUT
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        container = QWidget()
        container.setStyleSheet("background: transparent;") 
        main_layout.addWidget(container)

        outer_layout = QVBoxLayout()
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setSpacing(18)
        container.setLayout(outer_layout)

        # LOGO
        logo_label = QLabel("CAR RENTAL")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("color: white; font-size: 34px; font-weight: bold; letter-spacing: 2px; background: transparent;")

        # ΚΑΡΤΑ ΕΓΓΡΑΦΗΣ
        card = QFrame()
        card.setObjectName("MainCard")
        card.setFixedWidth(390)
        card.setStyleSheet("""
            #MainCard {
                background-color: rgba(255, 255, 255, 200);
                border-radius: 24px;
            }
        """)

        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(35, 30, 35, 30)
        card_layout.setSpacing(12) 
        card.setLayout(card_layout)

        title = QLabel("CREATE ACCOUNT")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #334155; font-size: 18px; font-weight: 600; background: transparent; margin-bottom: 5px;")

        # STYLES ΓΙΑ ΤΑ INPUTS
        input_style = """
            QLineEdit {
                background-color: rgba(120, 120, 120, 40);
                color: #1f2937;
                border: none;
                border-bottom: 2px solid #64748b;
                padding: 10px;
                padding-right: 35px;
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: rgba(120, 120, 120, 70);
                border-bottom: 2px solid #22c55e;
            }
            
        """

        # INPUT FIELDS

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(input_style)

        self.firstName_input = QLineEdit()
        self.firstName_input.setPlaceholderText("First Name")
        self.firstName_input.setStyleSheet(input_style)

        self.surname_input = QLineEdit()
        self.surname_input.setPlaceholderText("Last Name")
        self.surname_input.setStyleSheet(input_style)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email Address")
        self.email_input.setStyleSheet(input_style)

        self.phoneNumber_input = QLineEdit()
        self.phoneNumber_input.setPlaceholderText("Phone Number")
        self.phoneNumber_input.setStyleSheet(input_style)

        self.licenseNumber_input = QLineEdit()
        self.licenseNumber_input.setPlaceholderText("License Number")
        self.licenseNumber_input.setStyleSheet(input_style)

        self.licenseType_input = QLineEdit()
        self.licenseType_input.setPlaceholderText("License Type")
        self.licenseType_input.setStyleSheet(input_style)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(input_style)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm Password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet(input_style)
    
        # REGISTER BUTTON
        self.register_button = QPushButton("REGISTER")
        self.register_button.setMinimumHeight(48)
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #22c55e;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover { background-color: #16a34a; }
        """)

        # BACK TO LOGIN
        self.back_to_login = QPushButton("Already a member? Login")
        self.back_to_login.setCursor(Qt.PointingHandCursor)
        self.back_to_login.setStyleSheet("color: white; border: none; background: transparent; text-decoration: underline;")

        # ΠΡΟΣΘΗΚΗ ΣΤΑ LAYOUTS
        card_layout.addWidget(title)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.firstName_input)
        card_layout.addWidget(self.surname_input)
        card_layout.addWidget(self.email_input)
        card_layout.addWidget(self.phoneNumber_input)
        card_layout.addWidget(self.licenseNumber_input)
        card_layout.addWidget(self.licenseType_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.confirm_password_input)

        card_layout.addWidget(self.register_button)
        

        outer_layout.addWidget(logo_label)
        outer_layout.addWidget(card, alignment=Qt.AlignCenter)
        outer_layout.addWidget(self.back_to_login, alignment=Qt.AlignCenter)

        # ΣΥΝΔΕΣΕΙΣ
        self.register_button.clicked.connect(self.handle_register)
        
        self.showMaximized()

    def handle_register(self):
        username = self.username_input.text().strip() 
        firstName = self.firstName_input.text().strip()
        surname = self.surname_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm_pw = self.confirm_password_input.text().strip()
        licenseNumber = self.licenseNumber_input.text().strip()
        licenseType = self.licenseType_input.text().strip()
        phoneNumber = self.phoneNumber_input.text().strip()
        
        # 1. Έλεγχος κενών πεδίων
        if not all([username, firstName, surname, email, password, confirm_pw, licenseNumber, licenseType, phoneNumber]):
            QMessageBox.warning(self, "Σφάλμα", "Παρακαλώ συμπληρώστε όλα τα πεδία.")
            return

        # 2. Έλεγχος αν οι κωδικοί ταιριάζουν
        if password != confirm_pw:
            QMessageBox.warning(self, "Σφάλμα", "Οι κωδικοί δεν ταιριάζουν!")
            return
        # 3. Έλεγχος τύπου εισόδου
        # Εδώ στέλνεις τα δεδομένα στο back-end
        users = classes.User(username, password, "Customer", firstName, surname, email, phoneNumber, licenseNumber, licenseType)
        response = functions.RegisterUser(users)
        if response:
            print(f"Signing up: {username}, {email}")
            QMessageBox.information(self, "Επιτυχία", "Ο λογαριασμός δημιουργήθηκε!")
            self.user_window = LoginWindow()
            self.user_window.show()
            self.close()
        else:
            print(f"Error Signing up user!")
            QMessageBox.information(self, "Error!", "Ο λογαριασμός δεν δημιουργήθηκε!")

    def resizeEvent(self, event):
        if not self.original_pixmap.isNull():
            scaled_pixmap = self.original_pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
            self.bg_label.setPixmap(scaled_pixmap)
            self.bg_label.resize(self.size())
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec())