from PyQt5.QtWidgets import QMainWindow, QComboBox, QDateTimeEdit, QPushButton, QVBoxLayout, QWidget, QTableWidgetItem,\
    QTableWidget, QApplication, QLineEdit
from PyQt5.QtCore import QDateTime
from DB import DatabaseManager
import sys



class BookingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Book an Appointment")
        self.setGeometry(700, 300, 400, 300)
        self.db_manager = DatabaseManager()

        # Date and Time
        self.date_time_edit = QDateTimeEdit(self)
        self.date_time_edit.setDateTime(QDateTime.currentDateTime())  # Default time now

        # Choice services
        self.service_combo_box = QComboBox(self)

        # Choice masters
        self.master_combo_box = QComboBox(self)

        # Phone Number Field
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter your phone number before book")

        # Buttons
        self.check_availability_button = QPushButton("Check Availability", self)
        self.check_availability_button.clicked.connect(self.check_availability)

        self.book_button = QPushButton("Book Appointment", self)
        self.book_button.clicked.connect(self.book_appointment)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.clicked.connect(self.cancel_booking)

        layout = QVBoxLayout()
        layout.addWidget(self.date_time_edit)
        layout.addWidget(self.service_combo_box)
        layout.addWidget(self.master_combo_box)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.check_availability_button)
        layout.addWidget(self.book_button)
        layout.addWidget(self.cancel_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Populate services and masters after initializing widgets
        self.populate_services()
        self.service_combo_box.currentIndexChanged.connect(self.populate_masters)

    def populate_services(self):
        """Добавление услуг в выпадающий список"""
        self.service_combo_box.clear()
        services = self.db_manager.get_services()
        for service in services:
            self.service_combo_box.addItem(f"{service['ServiceName']}-{service['Duration']} min - ${service['Price']}",
                                           (service['ServiceID'], service['Duration']))
        # Вызов populate_masters для заполнения мастеров при запуске окна
        self.populate_masters()

    def populate_masters(self):
        """Добавление мастеров в выпадающий список в зависимости от выбранной услуги"""
        self.master_combo_box.clear()
        selected_service = self.service_combo_box.currentData()  # Получаем выбранную услугу
        if selected_service:
            service_id = selected_service[0]
            masters = self.db_manager.get_masters_for_service(service_id)
            for master in masters:
                rating = master['Rating']
                self.master_combo_box.addItem(f"{master['FirstName']} {master['LastName']}-⭐{rating}",
                                              master['MasterID'])




    def check_availability(self):
        """Check if master is available"""
        selected_master = self.master_combo_box.currentData()  # Take master ID
        start_time = self.date_time_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss")

        selected_service = self.service_combo_box.currentData()  # (ServiceID, Duration)
        service_duration = int(selected_service[1]) if selected_service else 30  # Default 30 min

        # Calculate end time
        end_time = self.date_time_edit.dateTime().addSecs(service_duration*60).toString("yyyy-MM-dd hh:mm:ss")

        is_available = self.db_manager.check_master_availability(selected_master, start_time, end_time)
        if is_available:
            self.db_manager.show_message("Available", "Master is available for the selected time!")
            return True
        else:
            self.db_manager.show_message("Unavailable", "Master is not available at this time.")
            return False

    def book_appointment(self):
        selected_master = self.master_combo_box.currentData()  # MasterID
        selected_service = self.service_combo_box.currentData()  # (ServiceID, Duration)
        service_id = selected_service[0]
        service_duration = int(selected_service[1]) if selected_service else 30  # Default 30 min

        start_time = self.date_time_edit.dateTime().toString("yyyy-MM-dd hh:mm:ss")
        end_time = self.date_time_edit.dateTime().addSecs(service_duration*60).toString("yyyy-MM-dd hh:mm:ss")

        client_phone = self.phone_input.text()
        if not client_phone:
            self.db_manager.show_message("Error", "Please enter your phone number.")
            return

        client_id = self.db_manager.get_client_id(client_phone)
        if client_id is None:
            self.db_manager.show_message("Error", "Client not found.")
            return

        if self.check_availability():
            success = self.db_manager.book_appointment(selected_master, client_id, service_id, start_time, end_time)
            if success:
                self.db_manager.show_message("Success", "Booking confirmed!")
            else:
                self.db_manager.show_message("Error", "Failed to book appointment.")
        else:
            self.db_manager.show_message("Error", "Мастер недоступен!")

    def cancel_booking(self):
        """Cancel booking"""
        client_phone = self.phone_input.text()
        if not client_phone:
            self.db_manager.show_message("Error", "Please enter your phone number.")
            return

        client_id = self.db_manager.get_client_id(client_phone)
        if client_id is None:
            self.db_manager.show_message("Error", "Client not found.")
            return

        selected_service = self.service_combo_box.currentData()
        if not selected_service:
            self.db_manager.show_message("Error", "Please select a service.")
            return

        service_id = selected_service[0]

        success = self.db_manager.cancel_appointment(client_id, service_id)
        if success:
            self.db_manager.show_message("Cancelled", "Your booking has been cancelled.")
        else:
            self.db_manager.show_message("Error", "Failed to cancel booking.")

class MasterRatingWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Master Ratings")
        self.setGeometry(700, 300, 600, 400)
        self.db_manager = DatabaseManager()

        layout = QVBoxLayout()

        # Таблица для рейтингов мастеров
        self.rating_table = QTableWidget(self)
        self.rating_table.setRowCount(0)
        self.rating_table.setColumnCount(3)
        self.rating_table.setHorizontalHeaderLabels(["First Name", "Last Name", "Rating"])
        layout.addWidget(self.rating_table)

        self.populate_table()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def populate_table(self):
        masters = self.db_manager.get_masters()  # Получаем всех мастеров из базы данных
        self.rating_table.setRowCount(len(masters))
        for row, master in enumerate(masters):
            self.rating_table.setItem(row, 0, QTableWidgetItem(master['FirstName']))
            self.rating_table.setItem(row, 1, QTableWidgetItem(master['LastName']))
            self.rating_table.setItem(row, 2, QTableWidgetItem(str(master['Rating'])))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BookingWindow()
    window.show()
    app.exec_()
