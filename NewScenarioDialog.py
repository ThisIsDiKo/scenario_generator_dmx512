import sys
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
    QGridLayout
)

class CustomDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Scenario Settings")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.gridlayout = QGridLayout()
        self.txtRowsNumber = QLineEdit('0')
        self.txtColsNumber = QLineEdit('0')

        self.gridlayout.addWidget(QLabel('Type'), 1, 0)
        self.gridlayout.addWidget(QLabel('Square'), 1, 1)
        self.gridlayout.addWidget(QLabel('Rows'), 2, 0)
        self.gridlayout.addWidget(self.txtRowsNumber, 2, 1)
        self.gridlayout.addWidget(QLabel('Cols'), 3, 0)
        self.gridlayout.addWidget(self.txtColsNumber, 3, 1)


        self.layout = QVBoxLayout()
        self.layout.addLayout(self.gridlayout)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
