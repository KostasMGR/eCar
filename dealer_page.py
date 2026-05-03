import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QScrollArea, QFrame, QTableWidget, 
    QTableWidgetItem, QHeaderView, QStackedWidget, QButtonGroup, 
    QMessageBox, QLineEdit, QFormLayout, QDoubleSpinBox, QSpinBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from back_end import functions
from back_end import classes

class DealerWindow(QMainWindow):
    def __init__(self, session_email: str):
        super().__init__()
        self.session_email = session_email
        self.setWindowTitle("eCar Rental - Dealer Panel")
        self.resize(1280, 820)

        # Κεντρικό Widget με Gradient Background
        outer = QWidget()
        self.setCentralWidget(outer)
        outer_layout = QVBoxLayout(outer)
        outer_layout.setContentsMargins(18, 18, 18, 18)
        outer.setStyleSheet("QWidget { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e293b, stop:1 #334155); }")

        app_shell = QFrame()
        app_shell.setObjectName("AppShell")
        app_shell.setStyleSheet("QFrame#AppShell { background-color: #f0f4f3; border-radius: 20px; }")
        shell_layout = QHBoxLayout(app_shell)
        shell_layout.setContentsMargins(0, 0, 0, 0)
        shell_layout.setSpacing(0)
        outer_layout.addWidget(app_shell)

        # SIDEBAR
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame { background-color: #0f172a; border-top-left-radius: 20px; border-bottom-left-radius: 20px; }
            QPushButton {
                text-align: left; padding: 14px 22px; border: none;
                font-size: 14px; font-weight: 600; color: #94a3b8;
                background: transparent; border-left: 4px solid transparent;
            }
            QPushButton:hover { background-color: #1e293b; color: white; }
            QPushButton:checked { background-color: #1e293b; color: white; border-left: 4px solid #38bdf8; }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        logo = QLabel("Dealer Panel")
        logo.setStyleSheet("color: white; font-size: 22px; font-weight: 800; padding: 20px;")
        sidebar_layout.addWidget(logo)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)

        # Tabs βάσει αιτήματος[cite: 2]
        self.btn_dash = self.make_nav_btn("View Dashboard", True)
        self.btn_create = self.make_nav_btn("Create Car")
        self.btn_reservations = self.make_nav_btn("View Reservations")
        
        sidebar_layout.addWidget(self.btn_dash)
        sidebar_layout.addWidget(self.btn_create)
        sidebar_layout.addWidget(self.btn_reservations)
        sidebar_layout.addStretch()

        shell_layout.addWidget(sidebar)

        # MAIN CONTENT[cite: 2]
        self.pages = QStackedWidget()
        shell_layout.addWidget(self.pages)

        # Σύνδεση Buttons με Σελίδες
        self.btn_dash.clicked.connect(lambda: self.pages.setCurrentIndex(0))
        self.btn_create.clicked.connect(lambda: self.pages.setCurrentIndex(1))
        self.btn_reservations.clicked.connect(self.load_reservations_and_show)

        self.pages.addWidget(self.create_dashboard_page())
        self.pages.addWidget(self.create_add_car_page())
        self.pages.addWidget(self.create_reservations_page())

    def make_nav_btn(self, text, checked=False):
        btn = QPushButton(text)
        btn.setCheckable(True)
        btn.setChecked(checked)
        self.nav_group.addButton(btn)
        return btn

    def create_banner(self, title, subtitle):
        banner = QFrame()
        banner.setFixedHeight(140)
        banner.setStyleSheet("background: #1e293b; border-top-right-radius: 20px;")
        layout = QVBoxLayout(banner)
        t = QLabel(title)
        t.setStyleSheet("color: white; font-size: 26px; font-weight: bold;")
        st = QLabel(subtitle)
        st.setStyleSheet("color: #94a3b8; font-size: 13px;")
        layout.addWidget(t)
        layout.addWidget(st)
        return banner

    # 1. VIEW DASHBOARD[cite: 2]
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_banner("Dashboard", f"Welcome back, {self.session_email}"))
        
        msg = QLabel("Use the sidebar to manage your car fleet and monitor customer reservations.")
        msg.setStyleSheet("font-size: 16px; color: #475569; padding: 40px;")
        msg.setAlignment(Qt.AlignCenter)
        layout.addWidget(msg)
        layout.addStretch()
        return page

    # 2. CREATE CAR
    def create_add_car_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_banner("Add New Car", "Enter the vehicle specifications below."))

        form_container = QWidget()
        form_layout = QFormLayout(form_container)
        
        self.in_brand = QLineEdit()
        self.in_model = QLineEdit()
        self.in_year = QSpinBox()
        self.in_year.setRange(1900, 2026)
        self.in_plate = QLineEdit()
        self.in_price = QDoubleSpinBox()
        self.in_price.setRange(0, 5000)

        form_layout.addRow("Brand:", self.in_brand)
        form_layout.addRow("Model:", self.in_model)
        form_layout.addRow("Year:", self.in_year)
        form_layout.addRow("Plate:", self.in_plate)
        form_layout.addRow("Price/Day (€):", self.in_price)

        btn_save = QPushButton("Register Vehicle")
        btn_save.setStyleSheet("background: #10b981; color: white; padding: 10px; font-weight: bold;")
        btn_save.clicked.connect(self.handle_create_car)
        form_layout.addRow(btn_save)

        layout.addWidget(form_container)
        layout.addStretch()
        return page

    def handle_create_car(self):
        # Χρήση της κλάσης Car από το source 1[cite: 1, 2]
        new_car = classes.Car(
            brand=self.in_brand.text(),
            model=self.in_model.text(),
            prod_year=self.in_year.value(),
            plate=self.in_plate.text(),
            seats=5, doors=5, cc=1400, state="Available",
            desc="", fuel="Gasoline", trans="Manual",
            horsepower=100, imgPath="", 
            price=self.in_price.value(), availability=True
        )
        if functions.CreateCar(new_car): #[cite: 3]
            QMessageBox.information(self, "Success", "Vehicle added to fleet!")
        else:
            QMessageBox.warning(self, "Error", "Plate already exists or database error.")

    # 3. VIEW RESERVATIONS[cite: 2, 3]
    def create_reservations_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_banner("Reservations", "List of all car rentals."))

        self.res_table = QTableWidget(0, 5)
        self.res_table.setHorizontalHeaderLabels(["Res ID", "Car ID", "User ID", "Total Price", "Status"])
        self.res_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.res_table)
        return page

    def load_reservations_and_show(self):
        self.pages.setCurrentIndex(2)
        # Σημείωση: Χρησιμοποιούμε τη GetUserReservations ή παρόμοια από functions[cite: 3]
        reservations = functions.GetUserReservations(self.session_email)
        if reservations:
            self.res_table.setRowCount(0)
            for i, res in enumerate(reservations):
                self.res_table.insertRow(i)
                self.res_table.setItem(i, 0, QTableWidgetItem(str(res['reservation_id'])))
                self.res_table.setItem(i, 1, QTableWidgetItem(str(res['car_id'])))
                self.res_table.setItem(i, 2, QTableWidgetItem(str(res['user_id'])))
                self.res_table.setItem(i, 3, QTableWidgetItem(f"{res['total_price']} €"))
                self.res_table.setItem(i, 4, QTableWidgetItem(res['reservation_status']))