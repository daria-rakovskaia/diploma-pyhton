from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np

def preprocess_image(image_data: Image):
    """
    Предобработка изображения перед передачей в OCR

    :param image_data: Входное изображение
    :return: Обработанное изображение в формате байтов
    """
    # повышение яркости
    image = ImageEnhance.Brightness(image_data).enhance(2.7)
    # повышение контрастности
    image = ImageEnhance.Contrast(image).enhance(100)
    # повышение резкости
    image = image.filter(ImageFilter.SHARPEN)
    # перевод в оттенки серого (Grayscale)
    np_img = np.array(image.convert("L"))
    # жёсткая контрастность для бинаризации
    np_img = np.clip(3 * (np_img - 128) + 128, 0, 255).astype(np.uint8)
    # бинаризация изображения (черно-белое)
    _, binary = cv2.threshold(np_img, 180, 255, cv2.THRESH_BINARY_INV)
    # дилатация - расширение белых участков изображения
    kernel = np.ones((2, 2), np.uint8)
    dilated = cv2.dilate(binary, kernel, iterations=1)
    # инверсия цветов
    final = cv2.bitwise_not(dilated)
    # получение изображения в виде bytes
    success, buffer = cv2.imencode(".png", final)
    image_bytes = buffer.tobytes()
    return image_bytes
