from django.utils.translation import gettext_lazy as _


def validate_empty(self, form, lesson_type):
    error_messages = []

    def is_field_empty(field_name):
        return not form[lesson_type].cleaned_data.get(field_name)

    def is_entity_selected(form_name):
        return bool(self.request.POST.get(form_name))

    if lesson_type == 'text':
        fields = {
            'title': 'text_title',
            'description': 'text_description',
            'content': 'content',
            'selected': 'step-text',
        }
        keyword = _('reading')
    elif lesson_type == 'video':
        fields = {
            'title': 'video_title',
            'description': 'video_description',
            'content': 'video_file',
            'selected': 'step-video',
        }
        keyword = _('video')
    elif lesson_type == 'quiz' or lesson_type == 'test':
        lesson_type = 'quiz'
        fields = {
            'title': 'title',
            'selected': 'step-test'
        }
        keyword = _('test')

    def check_for_empty():
        empty_fields = []
        for i in fields:
            if i != "selected":
                empty_fields.append(is_field_empty(fields[i]))
        return empty_fields

    if not is_entity_selected(fields['selected']) and True in check_for_empty():
        error_messages.append(generate_message(keyword, 'empty_all'))
    elif is_entity_selected(fields['selected']) and False in check_for_empty():
        error_messages.append(generate_message(keyword, 'chosen_and_filled'))
    return error_messages


def generate_message(keyword, error_type):
    if error_type == 'empty_all':
        return _("Empty fields found. You should select {} from the list or create a new one").format(keyword)
    elif error_type == 'chosen_and_filled':
        return _("You should select {} from the list or create a new one").format(keyword)


# Пока в таком виде, при написании тестов может быть расширена
def validate_empty_for_update(form, lesson_type):
    if not form['step'].cleaned_data[lesson_type]:
        return [_('For editing you should select related content')]
