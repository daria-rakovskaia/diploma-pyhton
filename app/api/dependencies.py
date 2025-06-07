from app.repositories.s3_repository import S3Repository
from app.services.s3_service import S3Service
from app.core.config import settings

def get_s3_client() -> S3Service:
    """
    Создает и возвращает экземпляр S3Service

    :return: Экземпляр S3Service
    """
    repository = S3Repository(
        access_key=settings.aws_access_key_id,
        secret_key=settings.aws_secret_access_key,
        endpoint_url=settings.s3_endpoint_url,
        bucket_name=settings.s3_bucket_name,
        bucket_id=settings.s3_bucket_id
    )
    return S3Service(repository)
