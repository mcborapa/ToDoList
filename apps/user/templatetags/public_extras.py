from django import template
from django.template.defaultfilters import stringfilter
from todolist.complement import cleanhtml
import os

register = template.Library()

@register.filter
@stringfilter
def cort(value,cant):
	value = cleanhtml(value, [{'format':'br','replace':''}])
	if (len(value))>=cant:
		return '{}...'.format(os.path.basename(value)[0:cant])
	else:
		return value