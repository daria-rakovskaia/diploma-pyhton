from io import BytesIO
from app.repositories.s3_repository import S3Repository

class S3Service:
    """
    Сервисный слой для работы с S3 через репозиторий
    """
    def __init__(self, repository: S3Repository):
        """
        Инициализирует сервис с указанным репозиторием S3

        :param repository: Экземпляр S3Repository для взаимодействия с хранилищем
        """
        self.repository = repository

    async def upload_student_file(
            self,
            file_obj: BytesIO,
            year: int,
            module: int,
            student_id: int,
            assignment_id: int,
            file_name: str
    ):
        """
        Загружает файл студента в S3 по сформированному пути

        :param file_obj: Файл в памяти в формате BytesIO
        :param year: Год сдачи работы
        :param module: Номер учебного модуля
        :param student_id: ID студента
        :param assignment_id: ID задания
        :param file_name: Имя файла (например, "sample1.png")
        :return: Путь до папки (S3-директории), куда был загружен файл
        """
        folder_path = f"{year}/module_{module}/student_{student_id}/assignment_{assignment_id}"
        object_key = f"{folder_path}/{file_name}"
        await self.repository.upload_file(file_obj, object_key)
        return folder_path
