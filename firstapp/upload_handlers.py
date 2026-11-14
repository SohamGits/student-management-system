from django.conf import settings
from django.core.files.uploadhandler import FileUploadHandler, StopUpload


class UploadSizeLimitHandler(FileUploadHandler):
    def __init__(self, request=None):
        super().__init__(request)
        self.total_bytes = 0

    def receive_data_chunk(self, raw_data, start):
        self.total_bytes += len(raw_data)
        if self.total_bytes > settings.MAX_UPLOAD_BYTES:
            self.request.upload_too_large = True
            raise StopUpload(connection_reset=True)
        return raw_data

    def file_complete(self, file_size):
        return None
