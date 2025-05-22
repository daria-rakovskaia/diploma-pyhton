from fastapi import UploadFile
from typing import Tuple, List
from PIL import Image
from io import BytesIO
from app.utils.image_processing import preprocess_image
from app.utils.paddle_ocr import process_ocr
from app.services.s3_service import S3Service

async def handle_ocr_image(
        image: UploadFile,
        s3_service: S3Service,
        year: int,
        module: int,
        student_id: int,
        assignment_id: int,
        file_index: int
) -> Tuple[List[str], str]:
    """
    Обрабатывает изображение: сохраняет в S3, выполняет OCR и возвращает распознанный текст

    :param image: Загруженный файл
    :param s3_service: Экземпляр сервиса для работы с S3
    :param year: Год сдачи работы
    :param module: Номер модуля
    :param student_id: ID студента
    :param assignment_id: ID задания
    :param file_index: Порядковый номер изображения
    :return: Кортеж из списка распознанных строк и S3-пути к файлу
    """
    contents = await image.read()
    original_stream = BytesIO(contents)

    original_stream.seek(0)
    object_key = await s3_service.upload_student_file(
        file_obj=original_stream,
        year=year,
        module=module,
        student_id=student_id,
        assignment_id=assignment_id,
        file_name=f"sample{file_index}.png"
    )

    original_stream.seek(0)
    image_pil = Image.open(original_stream)
    preprocessed_image = preprocess_image(image_pil)

    ocr_results = process_ocr(preprocessed_image)
    image_result = [line[1][0] for res in ocr_results for line in res]

    image_pil.close()
    original_stream.close()

    return image_result, object_key
