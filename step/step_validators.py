from django.shortcuts import render


def text_validate(self, form):
    text_title = self.request.POST.get('text_title')
    text_description = self.request.POST.get('text_description')
    content = self.request.POST.get('content')
    error_messages = []
    if len(text_title) < 1:
        error_messages.append("Название текста не может быть пустым")
    elif len(text_title) < 4:
        error_messages.append("Название текста должно быть длиной более 4 символов")
    if len(text_description) < 1:
        error_messages.append("Описание текста не может быть пустым")
    elif len(text_description) < 10:
        error_messages.append("Описание текста должно быть длиной более 10 символов")
    if len(content) < 1:
        error_messages.append("Содержимое текста не может быть пустым")
    elif len(content) < 50:
        error_messages.append("Содержимое текста должно быть длиной более 50 символов")
    if error_messages:
        return render_error(self, form, ", ".join(error_messages))
    return None


def video_validate(self, form):
    CONTENTTYPES = ['video/mp4',
                    'video/x-msvideo']
    error_messages = []
    video_title = self.request.POST.get('text_title')
    video_description = self.request.POST.get('text_description')
    current_file = self.cleaned_data.get("video_file", False)
    if current_file.content_type in CONTENTTYPES:
        if current_file.size > 2097152000:
            error_messages.append("Содержимое текста должно быть длиной более 50 символов")
    else:
        error_messages.append("Необходимо загрузить видео в формате MP4 или AVI")
    if len(video_title) < 1:
        error_messages.append("Название видео не может быть пустым")
    elif len(video_title) < 4:
        error_messages.append("Название видео должно быть длиной более 4 символов")
    if len(video_description) < 1:
        error_messages.append("Описание видео не может быть пустым")
    elif len(video_description) < 10:
        error_messages.append("Описание видео должно быть длиной более 10 символов")
    if error_messages:
        return render_error(self, form, ", ".join(error_messages))
    return None


def quiz_validate(self, form):
    questions_created = int(self.request.POST.get("question_blocks_count"))
    questions_qty = int(self.request.POST.get("test_questions_qty"))
    if questions_created < questions_qty:
        return render_error(self, form, "Количество создаваемых вопросов не может быть меньше вопросов в тесте")
    test_title = self.request.POST.get('test_title')
    test_questions_qty = self.request.POST.get('test_questions_qty')
    if len(test_title) < 1:
        return self.render_error(self, form, "Название теста не должно быть пустым")
    if len(test_questions_qty) < 1:
        return self.render_error(self, form, "Количество вопросов в тесте должно быть указано")
    for i in self.request.POST:
        if i.startswith('answers_qty'):
            if int(self.request.POST.get(i)) < 1:
                return self.render_error(self, form, "В вопросах должны быть ответы")
        if i.startswith('question_title'):
            if len(self.request.POST.get(i)) < 1:
                return self.render_error(self, form, "Вопросы не могут быть пустыми")
        if i.startswith('answer_'):
            if len(self.request.POST.get(i)) < 1:
                return self.render_error(self, form, "Ответы не могут быть пустыми")
    for i in range(1, questions_created + 1):
        answers_qty = sum(1 for j in range(1, 11) if self.request.POST.get(f'answer_{i}_{j}'))
        correct_answer_count = sum(
            1 for j in range(1, answers_qty + 1) if self.request.POST.get(f'is_correct_{i}_{j}') == 'True')
        if correct_answer_count > 1:
            return self.render_error(self, form, f"Не может быть более одного правильного ответа (Вопрос {i})")
        if correct_answer_count == 0:
            return self.render_error(self, form, f"Должен быть хотя бы один правильный ответ (Вопрос {i})")


def render_error(self, form, error_message):
    return render(self.request, self.template_name, {'form': form, 'error_message': error_message,
                                                     'returned': get_returning_context(self)})


def get_returning_context(self):
    context_to_return = {}
    lesson_type = self.request.POST.get('lesson_type')
    if lesson_type == 'text' or lesson_type == 'video':
        context_to_return[f'{lesson_type}_title'] = self.request.POST.get('text_title')
        context_to_return[f'{lesson_type}_description'] = self.request.POST.get('text_description')
        if lesson_type == 'text':
            context_to_return['content'] = self.request.POST.get('content')
        elif lesson_type == 'video':
            context_to_return['video_file'] = self.request.POST.get('video_file')
    elif lesson_type == 'test':
        question_blocks_count = int(self.request.POST.get('question_blocks_count'))
        for i in range(1, question_blocks_count + 1):
            context_to_return[f'question_title_{i}'] = self.request.POST.get(f'question_title_{i}')
            answers_qty = 0
            for j in range(1, 11):
                answer_text = self.request.POST.get(f'answer_{i}_{j}')
                if answer_text:
                    answers_qty += 1
                context_to_return[f'answer_{i}_{j}'] = answer_text
                context_to_return[f'is_correct_{i}_{j}'] = self.request.POST.get(f'is_correct_{i}_{j}')
    return context_to_return
