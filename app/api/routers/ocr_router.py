from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Dict, Any
import traceback

from app.api.dependencies import get_s3_client
from app.services.ocr_service import handle_ocr_image
from app.services.s3_service import S3Service
from app.services.postprocess_service import PostProcessService
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["OCR"])

@router.post("/recognize")
async def recognize_text(
    images: List[UploadFile] = File(..., description="Image file (JPG/PNG/БMP)"),
    year: int = Form(..., description="Год сдачи"),
    module: int = Form(..., description="Номер учебного модуля"),
    student_id: int = Form(..., description="Номер студента"),
    assignment_id: int = Form(..., description="Номер задания"),
    s3_service: S3Service = Depends(get_s3_client)
):
    """
    Загруженные изображения проходят проверку типа, отправляются в обработчик OCR, а затем сохраняются
    в хранилище S3

    :param images: Список загруженных изображений
    :param year: Год сдачи задания
    :param module: Учебный модуль
    :param student_id: ID студента
    :param assignment_id: ID задания
    :param s3_service: Зависимость для работы с S3-хранилищем
    :return: Список результатов распознавания и путь работы в хранилище
    """
    results = []
    work_url = None
    file_index = 1

    for image in images:
        if not image.content_type.startswith("image/"):
            raise HTTPException(400, "Invalid file type")

        try:
            image_result, work_url = await handle_ocr_image(
                image=image,
                s3_service=s3_service,
                year=year,
                module=module,
                student_id=student_id,
                assignment_id=assignment_id,
                file_index=file_index
            )
            results.append(image_result)
            file_index += 1
        except Exception as e:
            traceback_str = traceback.format_exc()
            raise HTTPException(
                500,
                f"Processing error: {type(e).__name__}: {str(e)}\nTraceback:\n{traceback_str}"
            )

    return {
        "results": results,
        "work_url": work_url
    }

@router.post("/postprocess-text")
def postprocess_text(data: Dict[str, Any]):
    """
    Обрабатывает распознанный текст, используя сервис постобработки

    :param data: json, содержащий распознанный текст
    :return: Обработанный текст + путь к работе
    """
    postprocess_service = PostProcessService(api_key=settings.groq_api_key)
    response, work_url = postprocess_service.postprocess_text(data=data)
    return {
        "response": response,
        "work_url": work_url
    }
