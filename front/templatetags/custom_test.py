from django import template

register = template.Library()


@register.filter(name='make_text_for_text')
def make_text_for_text(count):
    if count == 1:
        return f'{count} тест'
    elif 5 > count > 1:
        return f'{count} теста'
    elif count > 5 or count == 0:
        return f'{count} тестов'
    else:
        return 'ошибка'


@register.filter(name='make_text_for_lessons')
def make_text_for_lessons(count):
    if count == 1:
        return f'{count} практический материал'
    elif 5 > count > 1:
        return f'{count} практических материала'
    elif count > 5 or count == 0:
        return f'{count} практический материалов'
    else:
        return 'ошибка'