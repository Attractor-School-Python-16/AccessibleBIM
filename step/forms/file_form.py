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
        widgets = {
            'file_title': forms.TextInput(attrs={'class': 'form-control'}),
            'lesson_file': forms.FileField(attrs={'class': 'form-control'})
        }
