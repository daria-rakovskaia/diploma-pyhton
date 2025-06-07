from io import BytesIO
from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from urllib.parse import quote

class S3Repository:
    """
    Репозиторий для работы с S3-хранилищем
    """
    def __init__(self, access_key, secret_key, endpoint_url, bucket_name, bucket_id):
        """
        Инициализирует репозиторий S3 с указанными параметрами подключения

        :param access_key: Ключ доступа к S3
        :param secret_key: Секретный ключ доступа к S3
        :param endpoint_url: URL эндпоинта S3
        :param bucket_name: Название бакета, в который осуществляется загрузка
        :param bucket_id: ID бакета, в который осуществляется загрузка
        """
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.bucket_id = bucket_id
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        """
        Асинхронный контекстный менеджер, создающий клиента для работы с S3

        :return: Объект клиента S3
        """
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_obj: BytesIO, object_key: str):
        """
        Загружает файл в S3 по указанному ключу

        :param file_obj: Файл в памяти в формате BytesIO
        :param object_key: Ключ объекта
        :return: RuntimeError: При ошибке загрузки в S3
        """
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_key,
                    Body=file_obj,
                )
        except ClientError as e:
            raise RuntimeError(f"S3 upload error: {e}")

    def gen_url(
            self,
            object_key: str
    ) -> str:
        """
        Генерирует URL объекта

        :param object_key: Ключ объекта
        :return: URL объекта
        """
        return f"{self.bucket_id}.selstorage.ru/{quote(object_key)}"
