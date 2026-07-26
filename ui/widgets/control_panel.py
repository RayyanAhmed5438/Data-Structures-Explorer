import os

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class ControlPanel(QWidget):

    chooseLibraryRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

    

        layout = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        choose_button = QPushButton("Choose Library")
        choose_button.clicked.connect(self.chooseLibraryRequested.emit)
        choose_button.setStyleSheet( """
                            background-color: rgb(55,55,55);
                            border: 1px solid rgb(80,80,80);
                            border-radius: 6px;
                            padding: 6px;
                """)

        self.library_label = QLabel("No library selected")

        self.application_label = QLabel("No application selected")

        library = QLabel("Library")
        library.setStyleSheet("""
                    font-size: 15px;
                    font-weight: bold;
                    color: rgb(220,220,220);
                """)


        

        
        

        hbox2.addWidget(library)
        hbox2.addWidget(self.library_label)

        layout.addWidget(self.application_label)
        layout.addLayout(hbox2)

        layout.addWidget(choose_button)
        layout.setSpacing(18)
        layout.setContentsMargins(15, 15, 15 ,15)
    
        layout.addStretch()

        self.setLayout(layout)



    def set_application(self, application):

        self.application_label.setText("Application : " + application.name)

    def set_library(self, path):
        self.library_label.setText(os.path.basename(path))
        self.library_label.setToolTip(path)