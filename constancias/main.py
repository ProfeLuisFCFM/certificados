from PyQt6.QtWidgets import QApplication
import sys
from ui.app import ConstanciasApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConstanciasApp()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())
