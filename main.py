from window import CFEWindow
from PyQt6.QtWidgets import QApplication

import sys

app = QApplication(sys.argv)

window = CFEWindow()
window.show()

app.exec()
