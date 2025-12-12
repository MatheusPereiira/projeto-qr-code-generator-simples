import sys
from PyQt6.QtWidgets import QApplication
from frontend.app import QRAppUI

def main():
    app=QApplication(sys.argv)
    window=QRAppUI()
    window.show()
    sys.exit(app.exec())

if __name__=='__main__':
    main()
