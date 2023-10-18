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
        keyword = 'текст'
    elif lesson_type == 'video':
        fields = {
            'title': 'video_title',
            'description': 'video_description',
            'content': 'video_file',
            'selected': 'step-video',
        }
        keyword = 'видео'
    elif lesson_type == 'quiz' or lesson_type == 'test':
        lesson_type = 'quiz'
        fields = {
            'title': 'title',
            'questions_qty': 'questions_qty',
            'selected': 'step-test'
        }
        keyword = 'тест'

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
        return f"Обнаружены пустые поля. Необходимо выбрать {keyword} или создать нов{'ое' if keyword=='видео' else 'ый'}"
    elif error_type == 'chosen_and_filled':
        return (f"Необходимо либо выбрать существующ{'ее' if keyword == 'видео' else 'ий'} {keyword}, либо создать "
                f"нов{'ое' if keyword == 'видео' else 'ый'}")


#Пока в таком виде, при написании тестов может быть расширена
def validate_empty_for_update(form, lesson_type):
    if not form['step'].cleaned_data[lesson_type]:
        return ["Для редактирования необходимо выбрать связанный контент"]