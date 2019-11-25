import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from GUI import Information, LoadPhoto, Menu, Wardrobe, WardrobePart
from Recognizer import ImageHandler
from threading import Thread
from tensorflow.keras.models import load_model
from DataBase import MyClothes_database


class MenuWindow(QtWidgets.QMainWindow, Menu.Ui_MainWindow):
    info_window = ""
    load_photo_window = ""
    wardrobe_window = ""

    def __init__(self, parent=None):
        super(MenuWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_menu_to_load_photo)
        self.pushButton_2.clicked.connect(self.from_menu_to_wardrobe)
        self.pushButton_3.clicked.connect(self.from_menu_to_info)
        self.pushButton_4.clicked.connect(self.close_app)

    def from_menu_to_load_photo(self):
        self.load_photo_window = LoadPhotoWindow()
        self.load_photo_window.show()
        self.close()

    def from_menu_to_wardrobe(self):
        self.wardrobe_window = WardrobeWindow()
        self.wardrobe_window.show()
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
        self.pushButton_2.setEnabled(False)
        self.pushButton.clicked.connect(self.from_load_photo_to_menu)
        self.lineEdit.textChanged.connect(self.init_image_name)
        self.pushButton_3.clicked.connect(self.load_image)
        self.pushButton_2.clicked.connect(self.start_recognizing_thread)

    def init_image_name(self):
        self.pushButton_2.setEnabled(False)
        if self.lineEdit.text():
            self.image_name = self.image_directory + self.lineEdit.text()

    def load_image(self):
        pixmap = QPixmap(self.image_name)
        if not pixmap.isNull():
            self.label_3.setPixmap(pixmap.scaled(self.label_3.width(), self.label_3.height()))
            self.pushButton_2.setEnabled(True)
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
        image_handler = ImageHandler.ImageHandler()
        image_handler.model = self.model
        result = image_handler.recognizer(self.lineEdit.text())
        self.label_4.setText(str(result))
        database = MyClothes_database.DataBase()
        database.add_to_wardrobe(result, self.lineEdit.text())


class WardrobeWindow(QtWidgets.QMainWindow, Wardrobe.Ui_MainWindow):
    out_menu_window = ""

    def __init__(self, parent=None):
        super(WardrobeWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_wardrobe_to_menu)
        self.pixmap_t_shirt = QPixmap("GUI/WardrobeIcons/Tshirts.jpg")
        self.pixmap_trouser = QPixmap("GUI/WardrobeIcons/Trousers.jpg")
        self.pixmap_pullover = QPixmap("GUI/WardrobeIcons/Pullovers.jpg")
        self.pixmap_dress = QPixmap("GUI/WardrobeIcons/Dresses.jpg")
        self.pixmap_coat = QPixmap("GUI/WardrobeIcons/Overclothes.jpg")
        self.pixmap_shoes = QPixmap("GUI/WardrobeIcons/Shoes.jpg")
        self.pixmap_shirt = QPixmap("GUI/WardrobeIcons/Shirts.JPG")
        self.pixmap_bag = QPixmap("GUI/WardrobeIcons/Bags.jpg")
        self.label_11.setPixmap(self.pixmap_t_shirt.scaled(self.label_11.width(), self.label_11.height()))
        self.label_12.setPixmap(self.pixmap_trouser.scaled(self.label_12.width(), self.label_12.height()))
        self.label_13.setPixmap(self.pixmap_pullover.scaled(self.label_13.width(), self.label_13.height()))
        self.label_14.setPixmap(self.pixmap_dress.scaled(self.label_14.width(), self.label_14.height()))
        self.label_15.setPixmap(self.pixmap_coat.scaled(self.label_15.width(), self.label_15.height()))
        self.label_16.setPixmap(self.pixmap_shoes.scaled(self.label_16.width(), self.label_16.height()))
        self.label_17.setPixmap(self.pixmap_shirt.scaled(self.label_17.width(), self.label_17.height()))
        self.label_18.setPixmap(self.pixmap_bag.scaled(self.label_18.width(), self.label_18.height()))

    def from_wardrobe_to_menu(self):
        self.out_menu_window = MenuWindow()
        self.out_menu_window.show()
        self.close()


class WardrobePartWindow(QtWidgets.QMainWindow, WardrobePart.Ui_MainWindow):
    out_wardrobe_window = ""

    def __init__(self, parent=None):
        super(WardrobePartWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_wardrobe_part_to_wardrobe)

    def from_wardrobe_part_to_wardrobe(self):
        self.out_wardrobe_window = MenuWindow()
        self.out_wardrobe_window.show()
        self.close()

class TShirtsWindow(WardrobePartWindow):

    def __init__(self, wardrobe_part_name, pic_1, pic_2, pic_3, pic_4, pic_5, parent=None):
        super(WardrobePartWindow, self).__init__(parent)
        self.label_2.setText("T-shirts")
        self.label_11.setPixmap(pic_1)
        self.label_13.setPixmap(pic_2)
        self.label_15.setPixmap(pic_3)
        self.label_12.setPixmap(pic_4)
        self.label_15.setPixmap(pic_5)


class InfoWindow(QtWidgets.QMainWindow, Information.Ui_MainWindow):
    out_menu_window = ""

    def __init__(self, parent=None):
        super(InfoWindow, self).__init__(parent)
        self.setupUi(self)
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
