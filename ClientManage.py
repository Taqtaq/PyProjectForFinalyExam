from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton
from CreateEditDelete import ClientRegistrationWindow, EditUser, DeleteUser

class ClientManagementWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Client Management")
        self.setGeometry(700, 300, 400, 300)

        layout = QVBoxLayout

        # Buttons for client actions
        self.add_client_button = QPushButton("Add Client", self)
        self.add_client_button.clicked.connect(self.open_add_client_window)

        self.edit_client_button = QPushButton("Edit Client", self)
        self.edit_client_button.clicked.connect(self.open_edit_client_window)

        self.delete_client_button = QPushButton("Delete Client", self)
        self.delete_client_button.clicked.connect(self.open_delete_client_window)

        layout = QVBoxLayout()
        # Adding buttons to layout
        layout.addWidget(self.add_client_button)
        layout.addWidget(self.edit_client_button)
        layout.addWidget(self.delete_client_button)

        # Set layout in QWidget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_add_client_window(self):
        self.add_client_window = ClientRegistrationWindow()
        self.add_client_window.show()

    def open_edit_client_window(self):
        self.edit_client_window = EditUser()
        self.edit_client_window.show()

    def open_delete_client_window(self):
        self.delete_client_window = DeleteUser()
        self.delete_client_window.show()