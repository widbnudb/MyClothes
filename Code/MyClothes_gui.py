import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap
from GUI import Information, LoadPhoto, Menu, Wardrobe, WardrobePart
from Recognizer import ImageHandler
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
        self.pushButton_2.clicked.connect(self.start_recognizing)

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

    def start_recognizing(self):
        image_handler = ImageHandler.ImageHandler()
        image_handler.model = self.model
        result = image_handler.recognizer(self.lineEdit.text())
        self.label_4.setText(str(result))
        database = MyClothes_database.DataBase()
        database.add_to_wardrobe(result, self.lineEdit.text())


class WardrobeWindow(QtWidgets.QMainWindow, Wardrobe.Ui_MainWindow):
    out_menu_window = ""
    wardrobe_part_window = ""
    database = ""

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
        self.pushButton_2.clicked.connect(self.to_Tshirts)
        self.pushButton_3.clicked.connect(self.to_Trousers)
        self.pushButton_4.clicked.connect(self.to_Pullovers)
        self.pushButton_5.clicked.connect(self.to_Dresses)
        self.pushButton_6.clicked.connect(self.to_Coats)
        self.pushButton_7.clicked.connect(self.to_Shoes)
        self.pushButton_8.clicked.connect(self.to_Shirts)
        self.pushButton_9.clicked.connect(self.to_Bags)
        self.database = MyClothes_database.DataBase()

    def from_wardrobe_to_menu(self):
        self.out_menu_window = MenuWindow()
        self.out_menu_window.show()
        self.close()

    def to_Tshirts(self):
        self.wardrobe_part_window = WardrobePartWindow("T-shirts", self.database.get_from_db("T-shirt"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Trousers(self):
        self.wardrobe_part_window = WardrobePartWindow("Trousers", self.database.get_from_db("Trouser"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Pullovers(self):
        self.wardrobe_part_window = WardrobePartWindow("Pullovers", self.database.get_from_db("Pullover"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Dresses(self):
        self.wardrobe_part_window = WardrobePartWindow("Dresses", self.database.get_from_db("Dress"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Coats(self):
        self.wardrobe_part_window = WardrobePartWindow("Coats", self.database.get_from_db("Coat"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Shoes(self):
        self.wardrobe_part_window = WardrobePartWindow("Shoes", self.database.get_from_db("Shoes"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Shirts(self):
        self.wardrobe_part_window = WardrobePartWindow("Shirts", self.database.get_from_db("Shirt"))
        self.wardrobe_part_window.show()
        self.close()

    def to_Bags(self):
        self.wardrobe_part_window = WardrobePartWindow("Bags", self.database.get_from_db("Bag"))
        self.wardrobe_part_window.show()
        self.close()


class WardrobePartWindow(QtWidgets.QMainWindow, WardrobePart.Ui_MainWindow):
    out_wardrobe_window = ""

    def __init__(self, label_2, arg, parent=None):
        super(WardrobePartWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.from_wardrobe_part_to_wardrobe)
        self.label_2.setText(label_2)
        self.init_wardrobe_part(arg)

    def from_wardrobe_part_to_wardrobe(self):
        self.out_wardrobe_window = WardrobeWindow()
        self.out_wardrobe_window.show()
        self.close()

    def init_wardrobe_part(self, arg):
        if len(arg) > 0:
            self.label_11.setPixmap(QPixmap("Recognizer/Pictures/" + arg[0][0]).scaled(
                self.label_11.width(), self.label_11.height()))
        if len(arg) - 1 > 0:
            self.label_13.setPixmap(QPixmap("Recognizer/Pictures/" + str(arg[1][0])).scaled(
                self.label_11.width(), self.label_11.height()))
        if len(arg) - 2 > 0:
            self.label_15.setPixmap(QPixmap("Recognizer/Pictures/" + str(arg[2][0])).scaled(
                self.label_11.width(), self.label_11.height()))
        if len(arg) - 3 > 0:
            self.label_12.setPixmap(QPixmap("Recognizer/Pictures/" + str(arg[3][0])).scaled(
                self.label_11.width(), self.label_11.height()))
        if len(arg) - 4 > 0:
            self.label_14.setPixmap(QPixmap("Recognizer/Pictures/" + str(arg[4][0])).scaled(
                self.label_11.width(), self.label_11.height()))


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
