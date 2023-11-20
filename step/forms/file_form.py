from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.translation import gettext_lazy as _

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


CONTENTTYPES = [
    'text/plain',
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
    'image/vnd.dwg',
    'image/vnd.dxf'
]


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = ['file_title', 'lesson_file']
        labels = {
            'file_title': _('Enter the name of the uploaded file'),
            'lesson_file': _('Upload a file'),
        }

    def clean_lesson_file(self):
        lesson_file = self.cleaned_data.get("lesson_file", False)

        if not lesson_file:
            return lesson_file

        if isinstance(lesson_file, UploadedFile):
            if lesson_file.content_type not in CONTENTTYPES:
                raise forms.ValidationError(_('Only PDF, TXT, DOC, DOCX, XLS, XLSX, RVT, RFA, DWG, DXF formats allowed'))

            if lesson_file.size > 214958080:
                raise forms.ValidationError(_('Uploaded file has to be no more than 250 MB'))

        return lesson_file

    def clean(self):
        data = self.cleaned_data
        file_title = self.cleaned_data.get("file_title")
        lesson_file = self.cleaned_data.get("lesson_file", False)
        if (file_title and lesson_file) or (not file_title and not lesson_file):
            return data
        else:
            raise forms.ValidationError(_("Both title and file are mandatory"))
