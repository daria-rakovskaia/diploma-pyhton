from paddleocr import PaddleOCR

ocr_engine = PaddleOCR(
    use_angle_cls=False,
    lang='en',
    det_model_dir='det_model',
    rec_model_dir='rec_model',
    use_gpu=False
)

def process_ocr(image_data: bytes):
    """
    Обработка изображения через PaddleOCR
    :param image_data: Изображение в формате байтов для подачи в OCR
    :return: Список с результатами OCR
    """
    return ocr_engine.ocr(image_data)
