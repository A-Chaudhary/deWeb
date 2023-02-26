from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import zipfile
from get_dns_entry import*
import codecs
from utilities import *

from PyQt5.QtWebEngineWidgets import *
from beaker import sandbox
from base64 import b64encode, b64decode

import io

from PyQt5.QtPrintSupport import *

import os
import sys
class MainWindow(QMainWindow):

    def navigate_to_url(self):
        blockchainURL = self.lineEdit.text()
        transaction = get_domain_tx(blockchainURL)
        acl = sandbox.get_indexer_client()
        websitedata = b64decode(acl.transaction(transaction)['transaction']['note'])
        zip_name = "temp.zip"
        decoded_webpage(zip_name, websitedata)
        zipfile.ZipFile(zip_name, "r").extractall("temp")
        file_path = os.path.join("/mnt/c/Users/saicv/Desktop/deWeb/temp", "index.html")
        print(file_path)
        local_url = QUrl.fromLocalFile(file_path)
        self.browser.load(local_url)
        

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Blockchain Web Browser" )
        self.browser = QWebEngineView()
        self.resize(2048, 768)

        navitoolbar = QToolBar("Navigation" )
        navitoolbar.setIconSize(QSize(16,16))
        self.addToolBar(navitoolbar)

        self.lineEdit = QLineEdit()
        navitoolbar.addWidget(self.lineEdit)
        self.lineEdit.returnPressed.connect(self.navigate_to_url)
        back_img = QIcon(os.path.join('assets' ,'forward.png' ))
        back_button = QAction(back_img, "Back" , self)
        back_button.triggered.connect(self.browser.back)
        navitoolbar.addAction(back_button)

        next_img = QIcon(os.path.join('assets' ,'backward.png' ))
        next_button = QAction(next_img, "Forward" , self)
        next_button.triggered.connect(self.browser.forward)
        navitoolbar.addAction(next_button)
        
        self.setCentralWidget(self.browser)
        self.show()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()