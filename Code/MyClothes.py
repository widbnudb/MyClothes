import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtCore, QtGui, QtWidgets
import Menu  # Это наш конвертированный файл дизайна
import Information
import LoadPhoto


class MenuWindow(QtWidgets.QMainWindow, Menu.Ui_MainWindow):
    info_window = ""
    load_photo_window = ""

    def __init__(self, parent=None):
        super(MenuWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_menu_to_load_photo)
        self.pushButton_3.clicked.connect(self.from_menu_to_info)
        self.pushButton_4.clicked.connect(self.close_app)

    def from_menu_to_load_photo(self):
        self.load_photo_window = LoadPhotoWindow()
        self.load_photo_window.show()
        self.close()

    def from_menu_to_info(self):
        self.info_window = InfoWindow()
        self.info_window.show()
        self.close()

    def close_app(self):
        self.close()


class LoadPhotoWindow(QtWidgets.QMainWindow, LoadPhoto.Ui_MainWindow):
    out_menu_window = ""

    def __init__(self, parent=None):
        super(LoadPhotoWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_load_photo_to_menu)

    def from_load_photo_to_menu(self):
        self.out_menu_window = MenuWindow()
        self.out_menu_window.show()
        self.close()


class InfoWindow(QtWidgets.QMainWindow, Information.Ui_MainWindow):
    out_menu_window = ""

    def __init__(self, parent=None):
        super(InfoWindow, self).__init__(parent)
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton.clicked.connect(self.from_info_to_menu)

    def from_info_to_menu(self):
        self.out_menu_window = MenuWindow()
        self.out_menu_window.show()
        self.close()


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    menu_window = MenuWindow()  # Создаём объект класса ExampleApp
    menu_window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()