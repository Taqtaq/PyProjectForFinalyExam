from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QLabel, QMessageBox
from DB import DatabaseManager
class ClientRegistrationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Registration")
        self.setGeometry(700, 300, 400, 300)  # x=100, y=100, ширина=400, высота=300

        # Layout
        layout = QVBoxLayout()

        # Fields for entering client data
        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText("First Name")
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText("Last Name")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Phone Number")

        # Buttons for saving, editing and deleting
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_client)

        # Adding to layout
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.save_button)

        # Set layout in QWidget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Initialize database manager
        self.db_manager = DatabaseManager()

    def save_client(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        phone = self.phone_input.text()

        if self.db_manager.add_client(first_name, last_name, email, phone):
            self.db_manager.show_message("Successfully!", "User added successfully!")
            print("Client added successfully!")
        else:
            self.db_manager.show_message("Error!", "User has been added!")
            print("Client already exists!")


class EditUser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Information Editing")
        self.setGeometry(700, 300, 400, 300)  # x=100, y=100, ширина=400, высота=300

        self.first_name_input = QLineEdit(self)
        self.first_name_input.setPlaceholderText("First Name")
        self.last_name_input = QLineEdit(self)
        self.last_name_input.setPlaceholderText("Last Name")
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")

        self.old_phone_label = QLabel("Old phone number:")
        self.old_phone_input = QLineEdit()

        self.new_phone_label = QLabel("New phone number:")
        self.new_phone_input = QLineEdit()

        self.submit_button = QPushButton("Edit", self)
        self.submit_button.clicked.connect(self.update_user)

        layout = QVBoxLayout()
        layout.addWidget(self.first_name_input)
        layout.addWidget(self.last_name_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.old_phone_label)
        layout.addWidget(self.old_phone_input)
        layout.addWidget(self.new_phone_label)
        layout.addWidget(self.new_phone_input)

        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        # Initialize database manager
        self.db_manager = DatabaseManager()

    def update_user(self):
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        email = self.email_input.text()
        old_phone = self.old_phone_input.text()
        new_phone = self.new_phone_input.text()
        if self.db_manager.edit_client(first_name, last_name, email, old_phone, new_phone):
            self.db_manager.show_message("Successfully!", "Clients information successfully edited!")
            print("Clients information edit successfully!")
        else:
            self.db_manager.show_message("Error!", "Users not found!")
            print("Client not found!")
        self.close()


class DeleteUser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Registration")
        self.setGeometry(700, 300, 400, 300)

        self.phone_label = QLabel("Phone number:")
        self.phone_input = QLineEdit()

        self.submit_button = QPushButton("Delete", self)
        self.submit_button.clicked.connect(self.delete_user)

        layout = QVBoxLayout()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.db_manager = DatabaseManager()

    def delete_user(self):
        phone = self.phone_input.text()
        if self.db_manager.delete_client(phone):
            self.db_manager.show_message("Successfully!", "Client deleted successfully!!")
            print("Client deleted successfully!")
        else:
            self.db_manager.show_message("Error!", "Client not found!")
            print("Client not found!")
        self.close()