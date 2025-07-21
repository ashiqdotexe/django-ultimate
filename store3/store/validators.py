from django.core.exceptions import ValidationError
def validate_file_size(file):
    max_size = 50
    if file.size > max_size*1024:
        return ValidationError(f'File size can not be more that {max_size} kb')