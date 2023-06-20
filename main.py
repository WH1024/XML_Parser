import ctypes
import os
import xml.etree.ElementTree as ET
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QTextEdit, QFileDialog, QMessageBox, \
    QListWidget, QLabel
from PyQt5.QtCore import Qt
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('XML Parser')

        self.brandIdLineEdit = QLineEdit('MAN', self)
        self.brandIdLineEdit.setGeometry(10, 10, 200, 40)

        self.ecuIdLineEdit = QLineEdit('ECU_ID', self)
        self.ecuIdLineEdit.setGeometry(220, 10, 200, 40)

        self.filePathLineEdit = QLineEdit(self)
        self.filePathLineEdit.setGeometry(10, 60, 680, 40)

        self.loadButton = QPushButton('Load', self)
        self.loadButton.setGeometry(700, 60, 80, 40)
        self.loadButton.clicked.connect(self.load_file)

        self.tagLineEdit = QLineEdit(self)
        self.tagLineEdit.setGeometry(10, 110, 680, 40)

        self.parseButton = QPushButton('Parse', self)
        self.parseButton.setGeometry(700, 110, 80, 40)
        self.parseButton.clicked.connect(self.parse_xml)

        self.parseSelectedButton = QPushButton('Parse Selected Tag', self)
        self.parseSelectedButton.setGeometry(10, 160, 200, 40)
        self.parseSelectedButton.clicked.connect(self.parse_selected_tag)

        self.tagListWidget = QListWidget(self)
        self.tagListWidget.setGeometry(10, 210, 200, 380)
        self.tagListWidget.itemClicked.connect(self.load_selected_tag)

        self.resultTextEdit = QTextEdit(self)
        # self.resultTextEdit.setGeometry(220, 160, 380, 430)
        self.resultTextEdit.setGeometry(220, 160, 560, 430)

        # self.resultListTextEdit = QTextEdit(self)
        # self.resultListTextEdit.setGeometry(610, 160, 180, 430)

        self.authorLabel = QLabel('Author: HWH    Date: 2023.6.10', self)
        self.authorLabel.setAlignment(Qt.AlignRight | Qt.AlignTop)
        self.authorLabel.setGeometry(self.resultTextEdit.x(), self.resultTextEdit.y() + self.resultTextEdit.height(),
                                      self.resultTextEdit.width(), 20)

        self.setWindowIcon(QIcon("icon.png"))
        app.setWindowIcon(QIcon("icon.png"))

        self.show()

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open file', '', 'XML files (*.xml)')
        if file_path:
            self.filePathLineEdit.setText(file_path)
            self.load_tags()

    def load_tags(self):
        file_path = self.filePathLineEdit.text()
        if os.path.isfile(file_path):
            try:
                tree = ET.parse(file_path)
            except ET.ParseError:
                QMessageBox.warning(self, 'Warning', 'Invalid file path or file format.', QMessageBox.Ok)
                return
            root = tree.getroot()
            tag_names = [elem.tag for elem in root.iter() if elem.tag.startswith('SEG')]
            self.tagListWidget.clear()
            self.tagListWidget.addItems(tag_names)

    def load_selected_tag(self, item):
        self.tagLineEdit.setText(item.text())

    def parse_xml(self):
        brand_id = self.brandIdLineEdit.text()
        ecu_id = self.ecuIdLineEdit.text()
        file_path = self.filePathLineEdit.text()
        tag_name = self.tagLineEdit.text()
        if not os.path.isfile(file_path):
            QMessageBox.warning(self, 'Warning', 'Please input a valid file path.', QMessageBox.Ok)
            return
        if not tag_name:
            QMessageBox.warning(self, 'Warning', 'Please input the tag name.', QMessageBox.Ok)
            return
        try:
            tree = ET.parse(file_path)
        except ET.ParseError:
            QMessageBox.warning(self, 'Warning', 'Invalid file path or file format.', QMessageBox.Ok)
            return
        root = tree.getroot()
        dtc_elements = root.findall('.//{}//DTC'.format(tag_name))
        result_str = ''
        result_items = []
        for dtc_elem in dtc_elements:
            dtc_code = dtc_elem.attrib.get('DTCCode', '')
            for child in dtc_elem:
                tag = child.tag.replace('X', '0x')
                text = child.text if child.text is not None else ''
                num_str = tag.split('0x')[1]
                result_str += f"{brand_id}\t{ecu_id}\t{tag}\t{num_str}\t{text}\n"
                result_items.append((brand_id, ecu_id, tag, num_str, text, dtc_code))
        self.resultTextEdit.clear()
        # self.resultListTextEdit.clear()
        self.resultTextEdit.append(result_str)
        # for item in result_items:
        #     self.resultListTextEdit.append(f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}")

    def parse_selected_tag(self):
        brand_id = self.brandIdLineEdit.text()
        ecu_id = self.ecuIdLineEdit.text()
        file_path = self.filePathLineEdit.text()
        tag_name = self.tagListWidget.currentItem().text()
        if not os.path.isfile(file_path):
            QMessageBox.warning(self, 'Warning', 'Please input a valid file path.', QMessageBox.Ok)
            return
        try:
            tree = ET.parse(file_path)
        except ET.ParseError:
            QMessageBox.warning(self, 'Warning', 'Invalid file path or file format.', QMessageBox.Ok)
            return
        root = tree.getroot()
        dtc_elements = root.findall('.//{}//DTC'.format(tag_name))
        result_str = ''
        result_items = []
        for dtc_elem in dtc_elements:
            dtc_code = dtc_elem.attrib.get('DTCCode', '')
            for child in dtc_elem:
                tag = child.tag.replace('X', '0x')
                text = child.text if child.text is not None else ''
                num_str = tag.split('0x')[1]
                result_str += f"{brand_id}\t{ecu_id}\t{tag}\t{num_str}\t{text}\n"
                result_items.append((brand_id, ecu_id, tag, num_str, text, dtc_code))
        self.resultTextEdit.clear()
        # self.resultListTextEdit.clear()
        self.resultTextEdit.append(result_str)
        # for item in result_items:
        #     self.resultListTextEdit.append(f"{item[0]}\t{item[1]}\t{item[2]}\t{item[3]}\t{item[4]}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.parse_xml()

if sys.platform.startswith('win'):
    # 将控制台应用程序转换为GUI（窗口）应用程序
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    ctypes.windll.kernel32.SetConsoleCtrlHandler(None, 1)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())