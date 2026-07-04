import aioboto3
from botocore.exceptions import (
    BotoCoreError,
    ConnectionError,
    HTTPClientError,
    NoCredentialsError,
)

from exceptions import S3ConnectionError, S3FileUploadError
from storages.interfaces import S3StorageInterface


class S3StorageClient(S3StorageInterface):
    def __init__(
        self,
        endpoint_url: str,
        public_url: str,
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str,
    ):
        self._endpoint_url = endpoint_url
        self._public_url = public_url
        self._bucket_name = bucket_name
        self._region = region
        self._session = aioboto3.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    async def upload_file(self, file_name: str, file_data: bytes | bytearray) -> None:
        try:
            params = {"service_name": "s3", "region_name": self._region}
            if self._endpoint_url:
                params["endpoint_url"] = self._endpoint_url

            async with self._session.client(**params) as client:
                await client.put_object(
                    Bucket=self._bucket_name,
                    Key=file_name,
                    Body=file_data,
                )
        except (ConnectionError, HTTPClientError, NoCredentialsError) as error:
            raise S3ConnectionError(
                f"Failed to connect to S3 storage: {error}"
            ) from error
        except BotoCoreError as error:
            raise S3FileUploadError(
                f"Failed to upload to S3 storage: {error}"
            ) from error

    async def get_file_url(self, file_name: str) -> str:
        return f"{self._public_url.rstrip('/')}/{file_name.lstrip('/')}"
