from django.core.exceptions import ValidationError
from django.conf import settings


def validate_file_size(value):
    if value.size > settings.MAX_FILE_UPLOAD_SIZE['50 MB']:
        raise ValidationError(f'File size cannot exceed {settings.MAX_FILE_UPLOAD_SIZE}')
    return True