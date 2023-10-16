

def validate_empty(self, form, lesson_type):
    error_messages = []
    match lesson_type:
        case "test":
            if not self.request.POST.get("step-test") and (not form['quiz'].cleaned_data['title'] or not form[
                    'quiz'].cleaned_data['questions_qty']):
                error_messages.append("Обнаружены пустые поля. Необходимо выбрать тест или создать новый")
                return list(error_messages)
            elif self.request.POST.get("step-test") and form['quiz'].cleaned_data['title']:
                error_messages.append("Необходимо либо выбрать существующий тест, либо создать новый")
                return list(error_messages)



