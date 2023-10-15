
def validate_answer(question, answer, is_correct):
    return check_for_errors(question,  answer, is_correct)

def check_for_errors(question, answer, is_correct):
    error_messages = []
    fields_validation = check_fields(answer, is_correct)
    error_messages += fields_validation
    error_messages.append(check_correct_answers_count(question, is_correct))
    return [i for i in error_messages if i is not None and i]


def check_correct_answers_count(question, is_correct):
    answers_count = question.answer_bim.count()
    correct_answers = question.answer_bim.all().filter(is_correct=True)
    if answers_count >= 3:
        if not correct_answers and not is_correct:
            error_message = ("В вопросе должен быть хотя бы один правильный ответ")
            return error_message
    if answers_count >= 2:
        if len(correct_answers) == 1 and is_correct:
            error_message = ("В вопросе не может быть более двух правильных ответов")
            return error_message
    return None


#проверка полей проводится здесь же, поскольку ValidationError и self.add_errors в форме не работают (форма не
# отображается), вероятно потому что не передается pk вопроса

def check_fields(answer, is_correct):
    errors = []
    if not answer:
        errors.append("Поле ответа на может быть пустым")
    if len(answer) < 2:
        errors.append("Ответ должен быть длиной не менее двух символов")
    if answer.isdigit():
        errors.append("bla")
    if not isinstance(is_correct, bool):
        errors.append("Поле верности ответа может принимать только булевые значения")
    return errors
