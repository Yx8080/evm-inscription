from PyQt5.QtWidgets import QApplication
import win_ui

if __name__ == '__main__':
    app = QApplication([])
    my_window = win_ui.Main_WIN()
    my_window.show()
    app.exec_()
