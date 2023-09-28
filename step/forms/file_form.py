from django import forms
from django.core.exceptions import ValidationError

from step.models import FileModel

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB - 104857600
# 250MB - 214958080
# 500MB - 429916160

CONTENTTYPES = ['text/plain',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document']


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = '__all__'
        labels = {
            'file_title': 'Введите наименование файла',
            'lesson_file': 'Загрузите файл',
        }

    def clean_lesson_file(self):
        current_file = self.cleaned_data.get("lesson_file", False)
        if current_file.content_type in CONTENTTYPES:
            if current_file.size <= 20971520:
                return current_file
            else:
                raise forms.ValidationError("Размер загружаемого файла не должен превышать 20 МБ")
        else:
            raise forms.ValidationError("Необходимо загрузить файл в формате PDF, TXT, DOC, DOCX, XLS, XLSX")
