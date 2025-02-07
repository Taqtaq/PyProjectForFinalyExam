from PyQt5.QtWidgets import QApplication,QMessageBox,QWidget,QGraphicsPixmapItem,QHBoxLayout,QVBoxLayout,QPushButton,QLabel,QLineEdit,QGraphicsView,QComboBox,QGridLayout,QFormLayout,QTabBar,QTabWidget,QCheckBox
import sqlite3
from PyQt5.QtGui import QPixmap
from PIL import Image
import re
from main import MainWindow
from PyQt5 import QtGui,QtChart

            #  ეს არის ადმინისტრარორსი ფანჯარა
class Administrator(QWidget):
    def __init__(self):
        super().__init__()
        
        self.window()
        self.setGeometry(300,300,1500,500)
        self.setWindowTitle("Administrator Window")
        layout=QVBoxLayout()
       
        # იქმნება თაბები
        statistic_tab=QWidget()
        self.setStyleSheet("background-color: shadow")
        statistic_tab.setGeometry(100,200,900,700)
        statistic_tab_layout=QVBoxLayout()
        conn =sqlite3.connect("beauty.db")
        cursor=conn.cursor()
        loop_count=0
        clinet_num=[]
        masters=[]
        cursor.execute("select max(MasterID) from Appointments")
        maxID=cursor.fetchone()[0]
        while True:
            loop_count+=1
            cursor.execute("""select FirstName,LastName from Masters
                           where MasterID = {}
                           """.format(loop_count))
            try:
                names=cursor.fetchone()
                fname,lname=names[0],names[1]
                name=" ".join([fname,lname])
                
            except:
                continue
            
            cursor.execute("""select count(ClientID) from Appointments  
                       where MasterID = {}
                       """.format(loop_count))
            try:
                master_count=cursor.fetchone()[0]
            except:
                continue
                
            
            clinet_num.append(master_count)
            masters.append(name)
            if loop_count==maxID :
                break
                        
        chart=QtChart.QChart()
        
        chart.setTitle("Master's Clients")
        set0=QtChart.QBarSet("room1")
        set0.append(clinet_num)
        
        
        bar=QtChart.QBarSeries()
        bar.append(set0)
    
        
        x_axis=QtChart.QBarCategoryAxis()
        x_axis.append(masters)
        chart.setAxisX(x_axis,bar)
        
        y_axis=QtChart.QValueAxis()
    
        chart.setAxisY(y_axis,bar)
        y_axis.setRange(0,20)
        chart.legend().setVisible(True)
        chart.axisX().setTitleText("Masters")
        chart.axisY().setTitleText("Number of People")
        
        chart_view=QtChart.QChartView(chart)
        chart_view.setRenderHint(QtGui.QPainter.Antialiasing)
        chart_view.setStyleSheet("background-color:white")
        statistic_tab_layout.addWidget(chart_view)       
        
        
        
        
        statistic_label=QLabel()
        
        
        statistic_tab_layout.addWidget(statistic_label)
        statistic_tab.setLayout(statistic_tab_layout)
    
        
        
        
        export_info_tab=QWidget()
        info_type=QComboBox()
        info_type.addItems(['Choose Information','Masters','Services','Clients'])
        info_type.setFixedWidth(200)
        export_button=QPushButton("Export Information")
        
        
        export_label=QLabel()
        
        export_layout=QVBoxLayout()
        export_layout.addWidget(info_type)
        export_layout.addWidget(export_label)
        export_layout.addWidget(export_button)
        export_info_tab.setLayout(export_layout)
        
        tab=QTabWidget()
        tab.addTab(statistic_tab,"statistic")
        tab.addTab(export_info_tab,"export info")
        
        self.setTabOrder(statistic_tab,export_info_tab)
        
        
        
        export_button.clicked.connect(lambda:self.export_info(export_label,info_type.currentText()))
        
        layout.addWidget(tab)
    
        self.setLayout(layout)
    # ქმნის
    def create_statistic_table(self):
        
        layout=QVBoxLayout()
        self.button=QPushButton()
        self.info_type=QComboBox()
        self.info_type.addItems(['Choose information','Masters','Services','Clients'])
        self.info_type.resize(40,20)
        layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.show()
        
        # გამოაქვს  იმფორმაცია რომელიც დაკავშირებულია combobox-ში აირჩეულთან
    def export_info(self,label,info_type):
        
        conn=sqlite3.connect("beauty.db")
        cursor=conn.cursor()
        if info_type == 'Choose Information':
            label.clear()
        else:
            cursor.execute("""
                        select * from '{}'
                        """.format(info_type))
            label.clear()
            while True:
                a=cursor.fetchone()    
                if a!=None:
                    if info_type=="Masters":
                        label.setText(f"""{label.text()} \n  {a[0]}{(3-len(str(a[0])))*" "}  {a[1]}{(10-len(str(a[1])))*" "}  {a[2]}{(20-len(str(a[2])))*" "}  {a[3]}{(30-len(str(a[3])))*" "}  {a[4]}{3*" "}  {a[5]}{(10-len(str(a[5])))*" "}  {a[6]}""")
                    elif info_type=="Services":
                        label.setStyleSheet("font:48")
                        label.setText(f"""{label.text()} \n  {a[0]}{(3-len(str(a[0])))*" "} {a[1]}{(20-len(str(a[1])))*" "} {a[2]}ლ{(10-len(str(a[2])))*" "} {a[3]}წთ""")
                    elif info_type=="Clients":
                        label.setText(f"""{label.text()} \n  {a[0]}{(3-len(str(a[0])))*" "}  {a[1]}{(10-len(str(a[1])))*" "}  {a[2]}{(20-len(str(a[2])))*" "}  {a[3]}{(30-len(str(a[3])))*" "}  {a[4]}""")       
                        
                    
                else:
                    break
        conn.close()
        
        
        
        # ადმინისტრატორის გვერდზე შესასვლელი
class Check_Admin_Mail(QWidget):
    def __init__(self):
            super().__init__()
            self.window
            self.setWindowTitle("Beauty Salon")
            label=QLabel('Sign In')
            label.setStyleSheet("font:bold")
            
            
            mail_LineEdit=QLineEdit()
            mail_LineEdit.setPlaceholderText('Enter Your EMAIL')
            password_LineEdit=QLineEdit()
            password_LineEdit.setPlaceholderText('Enter Password')
            layout_form=QFormLayout()
            layout_form.addRow('Email:' ,mail_LineEdit)
            layout_form.addRow('Password:',password_LineEdit)
           
            
            
            
            sign_in_button=QPushButton("Sign In")
            button_layout=QGridLayout()
            
            button_layout.addWidget(sign_in_button,2,2)
            main_layout=QVBoxLayout()
            
            main_layout.addWidget(label)
            main_layout.addLayout(layout_form)
            main_layout.addLayout(button_layout)
         
        
            self.setLayout(main_layout)
            # ღილაკზე დაჭერის შემდეგ
            sign_in_button.clicked.connect(lambda:self.check_mail(mail_LineEdit.text(),password_LineEdit.text()))
        
        
        
            # ამოწმებს არის თუ არა ჩაწერილი მეილი და პაროი ადმინისტრატორის
    def check_mail(self,mail,password):
        conn=sqlite3.connect("beauty.db")
        cursor=conn.cursor()
        
        # არასწორი მეილის ან პაროლის შემთხვევაში გამოაქვს მესიჯი
        match_error=QMessageBox()
        match_error.setText("Your Email or Password is incorect!")
      
                #ადმინისტრატორია ის მეილები რომელთა ID ნაკლებია 6-ზე
                # ეძებს ID-ის
         
        cursor.execute("""
                           
                                select 'TRUE' from Admin
                                where Mail == "{}" and Password == "{}"  
                            
                            
                            """.format(str(mail),str(password)))
                        # ამოწმებს ID-ს
                    
            
            # ამით ვიჭერთ შეცდომას მაშინ როცა ჩაწერილი მეილი ან პაროლი არ ემთხვევა ბაზაში მყოფს
        try:
            return_message=cursor.fetchone()[0]
        except:
            # არასწორი მეილის ან პაროლის შემთხვევაში გამოაქვს მესიჯი
            match_error=QMessageBox()
            match_error.setText("Your Email or Password is incorect!")
            match_error.exec()
            return_message=False
            
            # ამოწმებს არსებობს თუ არა ისეთ ექაუნთი რომელის მეილი და პაროლი შეესაბამება მითითებულს
        if return_message :
                
            self.hide()
                    # ხსნის ახალ ფანჯარას
            self.window1=Administrator()
            self.window1.show()
            
        conn.close()
            
    

        # რეგისტრაციის ფანჯარა
class Register_window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Beauty Salon")
        policy_label=QLabel("check box if you agree your policy and conditions.")
        policy_label.setStyleSheet("")
        check_policy_and_conditions=QCheckBox()
        policy_layout=QHBoxLayout()
        policy_layout.addWidget(check_policy_and_conditions)
        policy_layout.addWidget(policy_label)
        
        register_button=QPushButton("Sign Up")
        register_button.setStyleSheet("background-color: grey")
           
        
        main_layout=QVBoxLayout()
        
        main_layout.addLayout(policy_layout)
        main_layout.addWidget(register_button)
        self.setLayout(main_layout)
        
        check_policy_and_conditions.clicked.connect(lambda:self.check_policy(check_policy_and_conditions,register_button))
    
    
    
        
         
    def check_policy(self,policy,button):
            policy.update()
            if policy.isChecked():
                button.setStyleSheet('background-color: blue ; color : white')
            else:
                button.setStyleSheet('background-color: grey ; color : black')

    
            
            
            
        #ეს არის შესასვლელი ფანჯარა
class Opening_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.window
        self.setWindowTitle("Beauty Salon")
        
        
        # კლიენტის ფანჯარაში გადასასვლელი ღილაკი
        log_in_button=QPushButton("Click To Continue")
        
        # ადმინისტრატორის შესასვლელში გადასასვლელი ფანჯარა
        adminButton=QPushButton()
        adminButton.setStyleSheet("border :0")
        main_label=QLabel()
        
        # ამატებს ფოტოს ფანჯარაში
        salon_picture=QPixmap('beauty-salon-logo.jpg')
        main_label.setPixmap(salon_picture)
        
        self.setStyleSheet("background-color:black")
        log_in_button.setStyleSheet("color:yellow;")
        
        # widget-ების განლაგება
        layout=QVBoxLayout()
        layout.addWidget(adminButton)
        layout.addWidget(main_label)
        layout.addWidget(log_in_button)
        
        self.setLayout(layout)
        
        adminButton.clicked.connect(lambda:self.open_admin_sign_up())
        log_in_button.clicked.connect(lambda:self.open_client_window())
        
        # ხსნის ადმინის შესასვლელ ფანჯარას
    def open_admin_sign_up(self):
        self.hide()
        self.admin_sign_up_window=Check_Admin_Mail()
        self.admin_sign_up_window.show()
       
        
        
        # ხსნის კლიენტის ფანჯარას
    def open_client_window(self):
        self.hide()
        self.window=MainWindow()
        self.window.show()   
        
        
        
        
                    
if __name__=="__main__":
    app=QApplication([])
    window=Opening_Window()
    window.show()
    app.exec()
    
