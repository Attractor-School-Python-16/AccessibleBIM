from django.shortcuts import render


def text_validate(self):
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
        return error_messages
    return None


def video_validate(self):
    CONTENTTYPES = ['video/mp4',
                    'video/x-msvideo']
    error_messages = []
    video_title = self.request.POST.get('video_title')
    video_description = self.request.POST.get('video_description')
    current_file = self.request.FILES.get("video_file")
    if not current_file:
        error_messages.append("Не загружен файл видео")
    else:
        if current_file.content_type in CONTENTTYPES:
            if current_file.size > 2097152000:
                error_messages.append("Размер файла видео не должен превышать 2 Гб")
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
        return error_messages
    return None


def quiz_validate(self):
    error_messages = []
    questions_qty = self.request.POST.get("test_questions_qty")
    questions_created = int(self.request.POST.get("question_blocks_count"))
    if questions_qty.isdigit() and len(questions_qty) >= 1:
        questions_qty = int(questions_qty)
        if questions_created < questions_qty:
            error_messages.append("Количество создаваемых вопросов не может быть меньше вопросов в тесте")
    else:
        error_messages.append("Количество вопросов в тесте должно быть указано и должно быть числом")
    test_title = self.request.POST.get('test_title')
    if len(test_title) < 1:
        error_messages.append("Название теста не должно быть пустым")
    for i in self.request.POST:
        if i.startswith('answers_qty'):
            if int(self.request.POST.get(i)) < 1:
                error_messages.append("В вопросах должны быть ответы")
        if i.startswith('question_title'):
            if len(self.request.POST.get(i)) < 1:
                error_messages.append("Вопросы не могут быть пустыми")
        if i.startswith('answer_'):
            if len(self.request.POST.get(i)) < 1:
                error_messages.append("Ответы не могут быть пустыми")
    for i in range(1, questions_created + 1):
        answers_qty = sum(1 for j in range(1, 11) if self.request.POST.get(f'answer_{i}_{j}'))
        correct_answer_count = sum(
            1 for j in range(1, answers_qty + 1) if self.request.POST.get(f'is_correct_{i}_{j}') == 'True')
        if correct_answer_count > 1:
            error_messages.append(f"Не может быть более одного правильного ответа (Вопрос {i})")
        if correct_answer_count == 0:
            error_messages.append(f"Должен быть хотя бы один правильный ответ (Вопрос {i})")
    if error_messages:
        return error_messages
    return None


def render_error(self, form, error_message):
    return render(self.request, self.template_name, {'form': form, 'error_message': error_message,
                                                     'returned': get_returning_context(self)})


def get_returning_context(self):
    context_to_return = {}
    lesson_type = self.request.POST.get('lesson_type')
    if lesson_type == 'text' or lesson_type == 'video':
        context_to_return[f'{lesson_type}_title'] = self.request.POST.get(f'{lesson_type}_title')
        context_to_return[f'{lesson_type}_description'] = self.request.POST.get(f'{lesson_type}_description')
        if lesson_type == 'text':
            context_to_return['content'] = self.request.POST.get('content')
            context_to_return['type_text'] = True
        elif lesson_type == 'video':
            context_to_return['video_file'] = self.request.FILES.get('video_file')
            context_to_return['type_video'] = True
    elif lesson_type == 'test':
        context_to_return['test_title'] = self.request.POST.get('test_title')
        question_blocks_count = int(self.request.POST.get('question_blocks_count'))
        for i in range(1, question_blocks_count + 1):
            context_to_return[f'question_title_{i}'] = self.request.POST.get(f'question_title_{i}')
            for j in range(1, 11):
                answer_text = self.request.POST.get(f'answer_{i}_{j}')
                if answer_text:
                    context_to_return[f'answer_{i}_{j}'] = answer_text
                    context_to_return[f'is_correct_{i}_{j}'] = self.request.POST.get(f'is_correct_{i}_{j}')
        context_to_return['type_test'] = True
        context_to_return['test_questions_qty'] = self.request.POST.get('test_questions_qty')
        context_to_return['questions_forms_qty'] = question_blocks_count
    print(context_to_return)
    return context_to_return
