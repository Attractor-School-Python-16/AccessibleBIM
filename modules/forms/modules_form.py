from django import forms

from modules.models import ModuleModel


class ModulesForm(forms.ModelForm):
    class Meta:
        model = ModuleModel
        fields = ['title', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
