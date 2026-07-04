class BaseS3StorageError(Exception):
    pass


class S3ConnectionError(BaseS3StorageError):
    pass


class S3FileUploadError(BaseS3StorageError):
    pass
