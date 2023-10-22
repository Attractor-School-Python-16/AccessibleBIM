from random import shuffle as shuffle_random

from django import template

register = template.Library()


@register.filter
def shuffle(arg):
    tmp = list(arg)[:]
    shuffle_random(tmp)
    return tmp
