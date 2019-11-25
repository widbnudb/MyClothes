from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras import utils
from keras.datasets import cifar10
import numpy as np
import winsound

# Загружаем данные
(x_train, y_train), (x_test, y_test) = fashion_mnist.load_data()
print(type(x_train))
# image = image / 255
# Список с названиями классов
classes = ['футболка', 'брюки', 'свитер', 'платье', 'пальто',
           'туфли', 'рубашка', 'кроссовки', 'сумка', 'ботинки']

# Преобразование размерности изображений
x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
# Нормализация данных
x_train = x_train / 255
x_test = x_test / 255

# Преобразуем метки в категории
y_train = utils.to_categorical(y_train, 10)
y_test = utils.to_categorical(y_test, 10)

# Создаем последовательную модель
model = Sequential()

# Добавляем уровни сети
model.add(Dense(900, input_dim=784, activation="relu"))
model.add(Dense(10, activation="softmax"))

# Компилируем модель
model.compile(loss="categorical_crossentropy",
              optimizer="SGD",
              metrics=["accuracy"])

print(model.summary())

# Обучаем сеть
history = model.fit(x_train, y_train,
                    batch_size=50,
                    epochs=200,
                    validation_split=0.2,
                    verbose=1)

# Оцениваем качество обучения сети на тестовых данных
scores = model.evaluate(x_test, y_test, verbose=1)
print("Доля верных ответов на тестовых данных, в процентах:", round(scores[1] * 100, 4))

model.save('fashion_mnist_dense.h5')





