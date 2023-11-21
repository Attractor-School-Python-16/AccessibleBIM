from django.utils.translation import gettext_lazy as _

from quiz_bim.models import AnswerBim


def validate_answer(form, question, answer, is_correct, update=False):
    return check_for_errors(form, question, answer, is_correct, update)


def check_for_errors(form, question, answer, is_correct, update):
    error_messages = []
    fields_validation = check_fields(answer, is_correct)
    error_messages += fields_validation
    error_messages.append(check_correct_answers_count(form, question, is_correct, update))
    return [i for i in error_messages if i is not None and i]


def check_correct_answers_count(form, question, is_correct, update):
    if update:
        instance_is_correct = AnswerBim.objects.get(id=form.instance.id).is_correct
    else:
        instance_is_correct = False
    error_message = None
    answers_count = question.answer_bim.count()
    correct_answers = question.answer_bim.all().filter(is_correct=True)
    # if answers_count >= 3:
    #     if not correct_answers and not is_correct or instance_is_correct and not is_correct:
    #         error_message = ("В вопросе должен быть хотя бы один правильный ответ")
    #         return error_message
    if answers_count >= 1:
        if correct_answers and is_correct:
            if not instance_is_correct:
                error_message = _("Question cannot have more than 2 right answers")
            return error_message
    return None


# проверка полей проводится здесь же, поскольку ValidationError и self.add_errors в форме не работают (форма не
# отображается), вероятно потому что не передается pk вопроса

def check_fields(answer, is_correct):
    errors = []
    if not answer:
        errors.append(_("Answer field cannot be empty"))
    if len(answer) < 2:
        errors.append(_("Answer should contain at least 2 symbols"))
    if is_correct is not True and is_correct is not False:
        errors.append(_("Answer correctness field can take only boolean values"))
    return errors
