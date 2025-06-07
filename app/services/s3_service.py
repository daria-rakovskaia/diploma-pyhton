import datetime
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
            check_date: datetime,
            student_id: int,
            work_code: int,
            assignment_id: int,
            file_name: str
    ):
        """
        Загружает файл студента в S3 по сформированному пути

        :param file_obj: Файл в памяти в формате BytesIO
        :param check_date: Дата проверки работы
        :param student_id: ID студента
        :param work_code: Код работы
        :param assignment_id: ID задания
        :param file_name: Имя файла (например, "sample1.png")
        :return: Путь до папки (S3-директории), куда был загружен файл
        """
        folder_path = f"{check_date}/student_{student_id}/work_code_{work_code}/assignment_{assignment_id}"
        object_key = f"{folder_path}/{file_name}"
        await self.repository.upload_file(file_obj, object_key)
        return folder_path

    def get_files_urls(
            self,
            file_num: int,
            object_key: str
    ):
        """
        Получает URL объекта

        :param file_num: Количество загруженных файлов
        :param object_key: Ключ объекта
        :return: URL объекта
        """
        url = self.repository.gen_url(object_key)
        urls = []
        for i in range(file_num):
            urls.append(f"https://{url}/sample{i + 1}.png")
        return urls
