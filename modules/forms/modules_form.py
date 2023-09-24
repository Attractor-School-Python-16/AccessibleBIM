from django import forms

from modules.models import ModuleModel


class ModulesForm(forms.ModelForm):
    class Meta:
        model = ModuleModel
        fields = ['title', 'description', 'image']
