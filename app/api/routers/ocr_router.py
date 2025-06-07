from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends, Query
from typing import List, Dict, Any
import traceback
from pydantic import BaseModel

from app.api.dependencies import get_s3_client
from app.services.ocr_service import handle_ocr_image
from app.services.s3_service import S3Service
from app.services.postprocess_service import PostProcessService
from app.core.config import settings
from app.services.analysis_service import AnalysisService

router = APIRouter(prefix="/api/v1", tags=["OCR"])

class FileUrlRequest(BaseModel):
    file_num: int
    object_key: str

class AnalysisRequest(BaseModel):
    task: str
    code: str

@router.post("/recognize")
async def recognize_text(
    images: List[UploadFile] = File(..., description="Image file (JPG/PNG/БMP)"),
    student_id: int = Form(..., description="Номер студента"),
    work_code: int = Form(..., description="Код работы"),
    assignment_id: int = Form(..., description="Номер задания"),
    s3_service: S3Service = Depends(get_s3_client)
):
    """
    Загруженные изображения проходят проверку типа, отправляются в обработчик OCR, а затем сохраняются
    в хранилище S3

    :param images: Список загруженных изображений
    :param student_id: ID студента
    :param work_code: Код работы
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
                check_date=datetime.today(),
                student_id=student_id,
                work_code=work_code,
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

@router.post("/get-file-url")
def get_file_url(
        request: FileUrlRequest,
        s3_service: S3Service = Depends(get_s3_client)
):
    """
    Получает URL объекта

    :param request: Количество загруженных файлов + Ключ объекта
    :param s3_service: Зависимость для работы с S3-хранилищем
    :return: URL объекта
    """
    try:
        return {"urls": s3_service.get_files_urls(request.file_num, request.object_key)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-code")
def analyze_code(request: AnalysisRequest):
    """
    Проводит анализ кода, используя сервис интеллектуального анализа кода

    :param request: Задача + код
    :return: Результат анализа
    """
    analysis_service = AnalysisService(api_key=settings.groq_api_key)
    response = analysis_service.analyze_code(task=request.task, code=request.code)
    return {
        "response": response
    }
