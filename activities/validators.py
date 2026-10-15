from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.deconstruct import deconstructible

@deconstructible
class FileSizeValidator:
    def __init__(self, max_mb=5, message=None):
        self.max_mb = max_mb
        self.message = message or f"File size cannot exceed {self.max_mb} MB."

    def __call__(self, value: UploadedFile):
        if value and value.size > self.max_mb * 1024 * 1024:
            raise ValidationError(self.message)

