'''ნიკა
1. რეგისტრაცია და კლიენტების მართვა:+++++
კლიენტების დასამატებლად/რედაქტირებისთვის ინტერფეისის შემუშავება.
დუბლიკატების შემოწმება და მონაცემების შემოწმება.
კლიენტების წაშლის ღილაკებისა და ფორმების დანერგვა.
2. დაჯავშნის სერვისები: -----
ფანჯარა თარიღისა და დროის ასარჩევად.
ოსტატების ხელმისაწვდომობის შემოწმების მექანიზმის დანერგვა.
ღილაკები ჯავშნის შეცვლის/გაუქმებისთვის.
3. მასტერ რეიტინგებთან მუშაობა: -----
ფანჯარა ოსტატების რეიტინგების სანახავად.
საუკეთესო ოსტატების ჩვენება ცხრილის სახით (QTableWidget).
4.ბაზის შექმნა მომსახურება-მასტერი+++++
'''


from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableWidget, QDialog, QLabel, QDateTimeEdit, QComboBox, \
                             QTableWidgetItem, QMessageBox, QVBoxLayout, QWidget, QLineEdit, QPushButton)
import sqlite3
import sys
from DB import DatabaseManager
from BookingWindow import BookingWindow, MasterRatingWindow
from CreateEditDelete import ClientRegistrationWindow, EditUser, DeleteUser
from ClientManage import ClientManagementWindow




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Menu")
        self.setGeometry(700, 300, 400, 300)

        layout = QVBoxLayout()

        # Buttons for choice book or client management
        self.booking_button = QPushButton("Booking System", self)
        self.booking_button.clicked.connect(self.open_booking_window)

        self.client_management_button = QPushButton("Manage Clients", self)
        self.client_management_button.clicked.connect(self.open_client_management_window)


        layout.addWidget(self.booking_button)
        layout.addWidget(self.client_management_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_booking_window(self):
        self.booking_window = BookingWindow()
        self.booking_window.show()

    def open_client_management_window(self):
        self.client_management_window = ClientManagementWindow()
        self.client_management_window.show()








if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
