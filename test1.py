import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, 
                             QTextEdit, QPushButton, QMessageBox, QFileDialog, 
                             QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
                             QFontComboBox, QSpinBox, QColorDialog)
from PyQt5.QtGui import QFont, QColor, QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt
import smtplib
from email.message import EmailMessage

class EmailApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Need to title")
        self.setGeometry(100, 100, 550, 720)
        
        self.file_paths = []  
        
    
        main_layout = QVBoxLayout(self)
        
      
        main_layout.addWidget(QLabel("Email (To - One after another):"))
        self.input_to = QLineEdit()
        self.input_to.setFixedHeight(30)
        main_layout.addWidget(self.input_to)
        
      
        main_layout.addWidget(QLabel("Subject:"))
        self.input_sub = QLineEdit()
        self.input_sub.setFixedHeight(30)
        main_layout.addWidget(self.input_sub)
        
       
        format_layout = QHBoxLayout()
        
      
        self.btn_bold = QPushButton("B")
        self.btn_bold.setFont(QFont("Arial", 10, QFont.Bold))
        self.btn_bold.setFixedWidth(35)
        self.btn_bold.setCheckable(True)
        self.btn_bold.clicked.connect(self.toggle_bold)
        format_layout.addWidget(self.btn_bold)
        
     
        self.btn_italic = QPushButton("I")
        font_i = QFont("Arial", 10)
        font_i.setItalic(True)
        self.btn_italic.setFont(font_i)
        self.btn_italic.setFixedWidth(35)
        self.btn_italic.setCheckable(True)
        self.btn_italic.clicked.connect(self.toggle_italic)
        format_layout.addWidget(self.btn_italic)
        
    
        self.btn_underline = QPushButton("U")
        font_u = QFont("Arial", 10)
        font_u.setUnderline(True)
        self.btn_underline.setFont(font_u)
        self.btn_underline.setFixedWidth(35)
        self.btn_underline.setCheckable(True)
        self.btn_underline.clicked.connect(self.toggle_underline)
        format_layout.addWidget(self.btn_underline)
        
     
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.set_font_family)
        format_layout.addWidget(QLabel("Fornt:"))
        format_layout.addWidget(self.font_combo)
        
       
        self.size_spin = QSpinBox()
        self.size_spin.setRange(8, 72)
        self.size_spin.setValue(12)
        self.size_spin.valueChanged.connect(self.set_font_size)
        format_layout.addWidget(QLabel("Size:"))
        format_layout.addWidget(self.size_spin)
        
       
        self.btn_color = QPushButton("Color (Color)")
        self.btn_color.clicked.connect(self.set_text_color)
        format_layout.addWidget(self.btn_color)
        
        main_layout.addLayout(format_layout)
        
       
        main_layout.addWidget(QLabel("Message):"))
        self.input_msg = QTextEdit()
        self.input_msg.setFixedHeight(140)
        self.input_msg.setFont(QFont("SolaimanLipi", 12))  
        main_layout.addWidget(self.input_msg)
        
      
        self.btn_attach = QPushButton("Attachment")
        self.btn_attach.setFixedHeight(35)
        self.btn_attach.clicked.connect(self.browse_file)
        main_layout.addWidget(self.btn_attach)
        
       
        main_layout.addWidget(QLabel("Attached Files:"))
        self.file_list_widget = QListWidget()
        self.file_list_widget.setFixedHeight(90)
        main_layout.addWidget(self.file_list_widget)
        
        
        self.btn_send = QPushButton("Send")
        self.btn_send.setFixedHeight(40)
        self.btn_send.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; font-size: 14px;")
        self.btn_send.clicked.connect(self.send_email)
        main_layout.addWidget(self.btn_send)

    
    def toggle_bold(self):
        fmt = QTextCharFormat()
        fmt.setFontWeight(QFont.Bold if self.btn_bold.isChecked() else QFont.Normal)
        self.merge_format_on_selection(fmt)

    def toggle_italic(self):
        fmt = QTextCharFormat()
        fmt.setFontItalic(self.btn_italic.isChecked())
        self.merge_format_on_selection(fmt)

    def toggle_underline(self):
        fmt = QTextCharFormat()
        fmt.setFontUnderline(self.btn_underline.isChecked())
        self.merge_format_on_selection(fmt)

    def set_font_family(self, font):
        fmt = QTextCharFormat()
        fmt.setFontFamily(font.family())
        self.merge_format_on_selection(fmt)

    def set_font_size(self, size):
        fmt = QTextCharFormat()
        fmt.setFontPointSize(size)
        self.merge_format_on_selection(fmt)

    def set_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            fmt = QTextCharFormat()
            fmt.setForeground(color)
            self.merge_format_on_selection(fmt)

    def merge_format_on_selection(self, format):
        cursor = self.input_msg.textCursor()
        if not cursor.hasSelection():
            cursor.select(QTextCursor.WordUnderCursor)
        cursor.mergeCharFormat(format)
        self.input_msg.mergeCurrentCharFormat(format)

    
    def browse_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select filesন", "", "All Files (*.*)")
        if files:
            for f in files:
                if f not in self.file_paths:
                    self.file_paths.append(f)
            self.update_file_list_ui()

    def update_file_list_ui(self):
        self.file_list_widget.clear()
        for index, path in enumerate(self.file_paths):
            file_name = os.path.basename(path)
            
            item_widget = QWidget()
            h_layout = QHBoxLayout(item_widget)
            h_layout.setContentsMargins(5, 2, 5, 2)
            
            label = QLabel(file_name)
            btn_remove = QPushButton("❌ Discard")
            btn_remove.setFixedSize(70, 25)
            btn_remove.setStyleSheet("color: red; font-weight: bold;")
            btn_remove.clicked.connect(lambda checked, p=path: self.remove_file(p))
            
            h_layout.addWidget(label)
            h_layout.addStretch()
            h_layout.addWidget(btn_remove)
            
            list_item = QListWidgetItem(self.file_list_widget)
            list_item.setSizeHint(item_widget.sizeHint())
            self.file_list_widget.setItemWidget(list_item, item_widget)

    def remove_file(self, path):
        if path in self.file_paths:
            self.file_paths.remove(path)
            self.update_file_list_ui()

     
    def send_email(self):
        recipient = self.input_to.text()
        subject = self.input_sub.text()
        
        content_html = self.input_msg.toHtml()
        content_plain = self.input_msg.toPlainText()
        
        if not recipient or not subject or not content_plain.strip():
            QMessageBox.warning(self, "সতর্কতা", "সবগুলো ঘর পূরণ করুন!")
            return

        try:
            msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = 'youremail@gmail.com'   
            msg['To'] = recipient
            
            msg.set_content(content_plain)
            msg.add_alternative(content_html, subtype='html')

            for path in self.file_paths:
                with open(path, 'rb') as f:
                    file_data = f.read()
                    file_name = os.path.basename(path)
                
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('youremail@gmail.com', 'AP Password') # give your AP Password
            server.send_message(msg)
            server.quit()

            QMessageBox.information(self, "successfull", "Has been sent!")
            
        except Exception as e:
            QMessageBox.critical(self, "ত্রুটি", f"ইমেইল পাঠানো যায়নি!\nএরর: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = EmailApp()
    ex.show()
    sys.exit(app.exec_())
