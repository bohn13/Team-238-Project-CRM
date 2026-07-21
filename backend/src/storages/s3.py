from inspect import isawaitable

import aioboto3
from botocore.exceptions import (
    BotoCoreError,
    ClientError,
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
        access_key: str,
        secret_key: str,
        bucket_name: str,
        region: str,
    ):
        self._endpoint_url = endpoint_url
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
        except (BotoCoreError, ClientError) as error:
            raise S3FileUploadError(
                f"Failed to upload to S3 storage: {error}"
            ) from error

    async def delete_file(self, file_name: str) -> None:
        try:
            params = {"service_name": "s3", "region_name": self._region}
            if self._endpoint_url:
                params["endpoint_url"] = self._endpoint_url

            async with self._session.client(**params) as client:
                await client.delete_object(
                    Bucket=self._bucket_name,
                    Key=file_name,
                )
        except (ConnectionError, HTTPClientError, NoCredentialsError) as error:
            raise S3ConnectionError(
                f"Failed to connect to S3 storage: {error}"
            ) from error
        except (BotoCoreError, ClientError) as error:
            raise S3FileUploadError(
                f"Failed to delete from S3 storage: {error}"
            ) from error

    async def generate_presigned_url(
        self, file_name: str, expires_in: int = 900
    ) -> str:
        params = {"service_name": "s3", "region_name": self._region}
        if self._endpoint_url:
            params["endpoint_url"] = self._endpoint_url
        try:
            async with self._session.client(**params) as client:
                url = client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self._bucket_name, "Key": file_name},
                    ExpiresIn=expires_in,
                )
                if isawaitable(url):
                    return await url
                return url
        except (ConnectionError, HTTPClientError, NoCredentialsError) as error:
            raise S3ConnectionError(
                f"Failed to connect to S3 storage: {error}"
            ) from error
        except (BotoCoreError, ClientError) as error:
            raise S3FileUploadError(
                f"Failed to generate S3 presigned URL: {error}"
            ) from error
