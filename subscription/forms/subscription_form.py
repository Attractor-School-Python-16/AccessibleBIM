from django import forms

from subscription.models import SubscriptionModel
from django.utils.translation import gettext_lazy as _


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionModel
        fields = ['course', 'price', 'is_published']
        labels = {
            'course': _('Course'),
            'price': _('Course price'),
            'is_published': _('Publish'),
        }

    def clean(self):
        course = self.cleaned_data.get("course")
        subscription = self.instance
        try:
            current_course = subscription.course
        except:
            current_course = None
        if course:
            if course.subscription.all() and course != current_course:
                raise forms.ValidationError(_(f"The subscription for course {course.title} already exists.\n Change or "
                                              f"delete existing subscription"))
        return super().clean()
