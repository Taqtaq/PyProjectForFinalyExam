import sqlite3
from PyQt5.QtWidgets import QMessageBox


class DatabaseManager:
    def __init__(self):
        self.conn = sqlite3.connect("beauty.db")
        self.conn.row_factory = sqlite3.Row  # Позволяет обращаться к результатам через ['FirstName']
        self.c = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def show_message(self, title, text, icon=QMessageBox.Information):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.exec_()

    def add_client(self, first_name, last_name, email, phone):
        # Проверка на дублирование
        self.c.execute("SELECT * FROM Clients WHERE Email=?", (email,))
        if self.c.fetchone():
            self.conn.commit()
            return False  # Дублирование найдено
        self.c.execute("INSERT INTO Clients (FirstName, LastName, Email, Phone) VALUES (?, ?, ?, ?)",
                       (first_name, last_name, email, phone))
        self.conn.commit()
        return True

    def edit_client(self, first_name, last_name, email, old_phone, new_phone):
        self.c.execute("SELECT * FROM Clients WHERE Phone=?", (old_phone,))
        if self.c.fetchone():
            self.c.execute("UPDATE Clients SET FirstName=?, LastName=?, Email=?, Phone=? WHERE Phone=?",
                           (first_name, last_name, email, new_phone, old_phone))
        else:
            return False
        self.conn.commit()
        return True

    def delete_client(self, phone):
        self.c.execute("SELECT * FROM Clients WHERE Phone=?", (phone,))
        if self.c.fetchone():
            self.c.execute("DELETE FROM Clients WHERE Phone=?", (phone,))
        else:
            return False
        self.conn.commit()
        return True

    def get_masters(self):
        self.c.execute("SELECT * FROM Masters")
        return self.c.fetchall()  # Возвращаем список всех мастеров

    def get_services(self):
        """Получение списка услуг из базы данных"""
        query = "SELECT ServiceID, ServiceName, Duration, Price FROM Services"
        return self.c.execute(query)

    def get_client_id(self, phone_number):
        try:
            self.c.execute("SELECT Client_id FROM Clients WHERE Phone=?", (phone_number,))
            result = self.c.fetchone()
            if result:
                return result['Client_id']
            return None
        except sqlite3.Error as e:
            print(f"Error getting client ID: {e}")
            return None

    def get_masters_for_service(self, service_id):
        """Возвращает мастеров, которые выполняют указанную услугу"""
        self.c.execute("""SELECT m.MasterID, m.FirstName, m.LastName, m.Rating 
                          FROM Masters m
                          JOIN MasterServices ms ON m.MasterID = ms.MasterID
                          WHERE ms.ServiceID = ?""", (service_id,))
        return self.c.fetchall()

    def get_services_for_master(self, master_id):
        """Возвращает услуги, которые выполняет указанный мастер"""
        self.c.execute("""SELECT s.ServiceID, s.ServiceName, s.Duration, s.Price 
                          FROM Services s
                          JOIN MasterServices ms ON s.ServiceID = ms.ServiceID
                          WHERE ms.MasterID = ?""", (master_id,))
        return self.c.fetchall()

    def check_master_availability(self, master_id, start_time, end_time):
        print(f"Checking availability in DB for Master {master_id}-id from {start_time} to {end_time}")
        self.c.execute("""SELECT * FROM Appointments
                   WHERE MasterID=? AND
                         ((StartTime BETWEEN ? AND ?) OR
                          (EndTime BETWEEN ? AND ?) OR
                          (? BETWEEN StartTime AND EndTime))""", (master_id, start_time, end_time, start_time, end_time, start_time))
        if self.c.fetchone():
            return False  # Мастер занят
        return True  # Мастер свободен

    def book_appointment(self, master_id, client_id, service_id, start_time, end_time):
        # Пишем запрос, чтобы создать запись о бронировании
        try:
            self.c.execute("""INSERT INTO Appointments (MasterID, ClientID, ServiceID, StartTime, EndTime) 
                           VALUES (?, ?, ?, ?, ?)""", (master_id, client_id, service_id, start_time, end_time))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def cancel_appointment(self, client_id, service_id):
        try:
            self.c.execute("DELETE FROM Appointments WHERE ClientID=? AND ServiceID=?", (client_id, service_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False




# # Create a table
# # Creating the Masters table
# c.execute("""CREATE TABLE IF NOT EXISTS Masters (
#         MasterID INTEGER PRIMARY KEY AUTOINCREMENT,
#         FirstName VARCHAR (50),
#         LastName VARCHAR (100),
#         Email VARCHAR (100) CHECK (Email LIKE '%@%'),
#         PhoneNumber VARCHAR(9) CHECK (PhoneNumber LIKE '555%' OR PhoneNumber LIKE '568%' \
#         OR PhoneNumber LIKE '579%' OR PhoneNumber LIKE '571%' OR PhoneNumber LIKE '599%' OR PhoneNumber LIKE '557%'),
#         Gender VARCHAR(10),
#         Rating FLOAT
#   )""")
# # Creating the Services table
# c.execute("""CREATE TABLE IF NOT EXISTS Services(
#     ServiceID INTEGER PRIMARY KEY AUTOINCREMENT,
#     ServiceName VARCHAR(50) CHECK (ServiceName IN ('Manicure','Hair cutting','Hairstyles','Massage')),
#     Price FLOAT N# # Connect to database
# # conn = sqlite3.connect("beauty.db")
# #
# # # row Factory
# # conn.row_factory = sqlite3.Row
# #
# # # Create a cursor
# # c = conn.cursor()OT NULL,
#     Duration INTEGER NOT NULL
# )""")
# # Creating the MasterServices table (associating masters with services)
# c.execute("""CREATE TABLE IF NOT EXISTS MasterServices(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     MasterID INTEGER,
#     ServiceID INTEGER,
#     FOREIGN KEY (MasterID) REFERENCES Masters(MasterID),
#     FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
# )""")
# c.execute("""CREATE TABLE IF NOT EXISTS Clients(
#     Client_id INTEGER PRIMARY KEY AUTOINCREMENT,
#     FirstName VARCHAR(50) NOT NULL,
#     LastName VARCHAR(100)NOT NULL,
#     Email VARCHAR(100) UNIQUE CHECK (Email LIKE '%@%'),
#     Phone VARCHAR(9) UNIQUE
#     CHECK (Phone LIKE '555%' OR
#            Phone LIKE '568%' OR
#            Phone LIKE '579%' OR
#            Phone LIKE '571%' OR
#            Phone LIKE '599%' OR
#            Phone LIKE '557%')
# )""")
# c.execute("""CREATE TABLE IF NOT EXISTS Appointments (
#     AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
#     MasterID INTEGER NOT NULL,
#     ClientID INTEGER NOT NULL,
#     ServiceID INTEGER NOT NULL,
#     StartTime VARCHAR(100) NOT NULL,
#     EndTime VARCHAR(100) NOT NULL,
#     FOREIGN KEY (MasterID) REFERENCES Masters(MasterID),
#     FOREIGN KEY (ClientID) REFERENCES Clients(Client_id),
#     FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
# )""")
# c.execute("DROP TABLE IF EXISTS Appointments")

# Adding employees to the Masters table
# masters_lst = [('Ani', 'Gabunia', 'ani.gabunia@gmail.com', '555123456', 'Female', 4.8),
#                ('Mariam', 'Bzhalava', 'mariam.bzhalava@gmail.com', '568987654', 'Female', 4.6),
#                ('Tamar', 'Chkheidze', 'tamar.chkheidze@gmail.com', '579112233', 'Female', 4.7),
#                ('Nino', 'Kiknadze', 'nino.kiknadze@gmail.com', '571334455', 'Female', 4.5),
#                ('Salome', 'Gogichaishvili', 'salome.gogichaishvili@gmail.com', '599445566', 'Female', 4.9),
#                ('Elene', 'Beridze', 'elene.beridze@gmail.com', '557556677', 'Female', 4.8),
#                ('Keti', 'Lomidze', 'keti.lomidze@gmail.com', '555667788', 'Female', 4.4),
#                ('Giorgi', 'Tsiklauri', 'giorgi.tsiklauri@gmail.com', '568778899', 'Male', 4.7),
#                ('Lasha', 'Kharshiladze', 'lasha.kharshiladze@gmail.com', '579889900', 'Male', 4.6),
#                ('Nikoloz', 'Kvirikashvili', 'nikoloz.kvirikashvili@gmail.com', '571990011', 'Male', 4.5)]
#
# c.executemany("""INSERT INTO Masters (FirstName, LastName, Email, PhoneNumber, Gender, Rating)
# VALUES (?,?,?,?,?,?)""", masters_lst)

# Adding services to the Services table
# List of services to be added to the Services table
# services_lst = [
#     ('Manicure', 25.0, 30),  # ServiceName, Price, Duration (in minutes)
#     ('Hair cutting', 40.0, 45),
#     ('Hairstyles', 50.0, 60),
#     ('Massage', 60.0, 75)
# ]

# Inserting multiple services into the Services table
# c.executemany("""INSERT INTO Services (ServiceName, Price, Duration)
# VALUES (?,?,?)""", services_lst)

# Linking employees with services in the MasterServices table
# c.execute("""
# INSERT INTO MasterServices (MasterID, ServiceID)
# VALUES
#     -- Massage therapists (4 employees)
#     (1, 4),
#     (2, 4),
#     (3, 4),
#     (4, 4),
#
#     -- Hairdressers (2 employees, cutting and styling)
#     (5, 2),
#     (5, 3),
#     (6, 2),
#     (6, 3),
#
#     -- Stylists (1 employee)
#     (7, 3),
#
#     -- Manicurists (3 employees)
#     (8, 1),
#     (9, 1),
#     (10, 1);
# """)
# clients_lst = [
#     ('Nino', 'Beridze', 'nino.beridze@gmail.com', '555123456'),
#     ('Giorgi', 'Papashvili', 'giorgi.papashvili@gmail.com', '568987654'),
#     ('Tamar', 'Jorjadze', 'tamar.jorjadze@gmail.com', '579112233')
# ]
#
# # Insert multiple clients into the Clients table
# c.executemany("""INSERT INTO Clients (FirstName, LastName, Email, Phone)
# VALUES (?,?,?,?)""", clients_lst)


# conn.commit()
