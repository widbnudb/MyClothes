import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from GUI import Information, LoadPhoto, Menu
from Recognizer import ImageHandler
from threading import Thread
from tensorflow.keras.models import load_model


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
    image_directory = "Recognizer/Pictures/"
    image_name = ""
    model = load_model('Recognizer/fashion_mnist_dense.h5')

    def __init__(self, parent=None):
        super(LoadPhotoWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_load_photo_to_menu)
        self.lineEdit.textChanged.connect(self.init_image_name)
        self.lineEdit.editingFinished.connect(self.load_image)
        self.pushButton_2.clicked.connect(self.start_recognizing_thread)

    def init_image_name(self):
        if self.lineEdit.text():
            self.image_name = self.image_directory + self.lineEdit.text()

    def load_image(self):
        pixmap = QPixmap(self.image_name)
        if not pixmap.isNull():
            self.label_3.setPixmap(pixmap.scaled(self.label_3.width(), self.label_3.height()))
        else:
            self.lineEdit.clear()

    def from_load_photo_to_menu(self):
        self.out_menu_window = MenuWindow()
        self.out_menu_window.show()
        self.close()

    def make_recognizing(self):
        thread = Thread(target=self.start_recognizing_thread())
        thread.start()
        thread.join()

    def start_recognizing_thread(self):
        print("1")
        image_handler = ImageHandler.ImageHandler()
        image_handler.model = self.model
        print("2")
        result = image_handler.recognizer(self.lineEdit.text())
        print("3")
        self.label_4.setText(str(result))
        #image_handler.addtoDB(self.image_name)


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
    app = QtWidgets.QApplication(sys.argv)
    menu_window = MenuWindow()
    menu_window.show()
    app.exec_()


if __name__ == '__main__':
    main()