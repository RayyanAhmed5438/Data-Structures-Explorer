import os

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout,QHBoxLayout, QPushButton
from PyQt5.QtCore import pyqtSignal


class ControlPanel(QWidget):


    def __init__(self):
        super().__init__()


        layout = QVBoxLayout()
       
    
        layout.addStretch()

        self.setLayout(layout)



    def set_application(self, application):

        self.application_label.setText("Application : " + application.name)
