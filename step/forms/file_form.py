from django import forms

from step.models import FileModel


class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        fields = '__all__'
        labels = {
            'file_title': 'Введите наименование файла',
            'lesson_file': 'Загрузите файл',
        }
