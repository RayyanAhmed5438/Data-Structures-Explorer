from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSplitter
)
from ui.widgets.control_panel import ControlPanel
from ui.widgets.visualization_panel import VisualizationPanel

class WorkspacePage(QWidget):

    backRequested = pyqtSignal()
    chooseLibraryRequested = pyqtSignal()

    def __init__(self):

        super().__init__()

        self.application = None

        self.setup_ui()

    def set_application(self, application):

        self.application = application

        self.control_panel.set_application(application)

    def setup_ui(self):

        main_layout = QVBoxLayout()

        back_button = QPushButton(" <- Home")
        back_button.clicked.connect(self.backRequested.emit)

        splitter = QSplitter()

        self.control_panel = ControlPanel()
        self.visualization_panel = VisualizationPanel()

        self.control_panel.chooseLibraryRequested.connect(
            self.chooseLibraryRequested.emit
        )

        splitter.addWidget(self.control_panel)
        splitter.addWidget(self.visualization_panel)

        splitter.setSizes([500, 500])

        splitter.setChildrenCollapsible(False)

        main_layout.addWidget(back_button)
        main_layout.addWidget(splitter)

    

        self.setLayout(main_layout)

    def visualize_array(self, array):
        self.visualization_panel.visualize_array(array)