from django import forms

from subscription.models import SubscriptionModel


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = SubscriptionModel
        fields = ['course', 'price', 'is_published']

    def clean(self):
        course = self.cleaned_data.get("course")
        subscription = self.instance
        try:
            current_course = subscription.course
        except:
            current_course = None
        if course:
            if course.subscription.all() and course != current_course:
                raise forms.ValidationError(f"Подписка на курс {course.title} уже существует.\n Измените или удалите "
                                            f"существующую подписку")
        return super().clean()
