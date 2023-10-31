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
# application/octet-stream - .nwf, .rte
# application/x-step .ifc
# application/xml  .ifcXML


CONTENTTYPES = ['text/plain',
                'application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/zip',
                'application/x-7z-compressed',
                'application/vnd.rar',
                'application/octet-stream',
                'application/x-step',
                'application/xml',
                ]


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file_title', 'lesson_file']
        labels = {
            'file_title': 'Введите наименование загружаемого файла',
            'lesson_file': 'Загрузите файл',
        }

    def clean_lesson_file(self):
        lesson_file = self.cleaned_data.get("lesson_file", False)
        if lesson_file:
            if lesson_file.content_type in CONTENTTYPES:
                if lesson_file.size <= 20971520:
                    return lesson_file
                else:
                    raise forms.ValidationError("Размер загружаемого файла не должен превышать 20 МБ")
            else:
                raise forms.ValidationError("Необходимо загрузить файл в формате PDF, TXT, DOC, DOCX, XLS, XLSX")
        else:
            return lesson_file

    def clean(self):
        data = self.cleaned_data
        file_title = self.cleaned_data.get("file_title")
        lesson_file = self.cleaned_data.get("lesson_file", False)
        if (file_title and lesson_file) or (not file_title and not lesson_file):
            return data
        else:
            raise forms.ValidationError("При загрузке документа требуется обязательно указать название")
