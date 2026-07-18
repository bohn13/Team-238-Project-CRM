from abc import ABC, abstractmethod


class S3StorageInterface(ABC):
    @abstractmethod
    async def upload_file(self, file_name: str, file_data: bytes | bytearray) -> None:
        pass

    @abstractmethod
    async def delete_file(self, file_name: str) -> None:
        pass

    @abstractmethod
    async def generate_presigned_url(
        self, file_name: str, expires_in: int = 900
    ) -> str:
        pass
