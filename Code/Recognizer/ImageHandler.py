import numpy as np
from PIL import Image, ImageFilter
from tensorflow.keras.models import load_model


class ImageHandler:
    def __init__(self):
        self.model = load_model('Recognizer/fashion_mnist_dense.h5')
        self.classes = ['T-shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
                   'Shoes', 'Shirt', 'Shoes', 'Bag', 'Shoes']

    def imageprepare(self, argv):
        im = Image.open(argv).convert('L')
        width = float(im.size[0])
        height = float(im.size[1])
        newImage = Image.new('L', (28, 28), (255))  # creates white canvas of 28x28 pixels
        if width > height:  # check which dimension is bigger
            # Width is bigger. Width becomes 20 pixels.
            nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
            if (nheight == 0):  # rare case but minimum is 1 pixel
                nheight = 1
                # resize and sharpen
            img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
            wtop = int(round(((28 - nheight) / 2), 0))  # calculate horizontal position
            newImage.paste(img, (4, wtop))  # paste resized image on white canvas
        else:
            # Height is bigger. Heigth becomes 20 pixels.
            nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
            if (nwidth == 0):  # rare case but minimum is 1 pixel
                nwidth = 1
                # resize and sharpen
            img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
            wleft = int(round(((28 - nwidth) / 2), 0))  # caculate vertical pozition
            newImage.paste(img, (wleft, 4))  # paste resized image on white canvas
        pixel_val = list(newImage.getdata())  # get pixel values
        # normalize pixels to 0 and 1. 0 is pure white, 1 is pure black.
        normal_pixel_val = [(255 - x) * 1.0 / 255.0 for x in pixel_val]
        return normal_pixel_val

    def recognizer(self, file_name):
        file_name = "Recognizer/Pictures/" + file_name
        x = self.imageprepare(file_name)
        image = np.asarray(x)
        image = image.reshape(1, 784)
        prediction = self.model.predict(image)
        np.argmax(prediction)
        return self.classes[int(np.argmax(prediction))]

