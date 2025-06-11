# projects/validators.py
from django.core.exceptions import ValidationError
import os

def validate_file_type(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.zip', '.doc', '.docx']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file type.')
        
def validate_file_size(value):
    filesize = value.size
    if filesize > 10*1024*1024:  # 10MB
        raise ValidationError("Maximum file size is 10MB")

# In models.py
file = models.FileField(
    upload_to='project_files/%Y/%m/%d/',
    validators=[validate_file_type, validate_file_size]
)
