from atexit import register
import imp
from django import template
from ..models import Test
import datetime
register=template.Library()
from django.template.defaultfilters import upper
import markdown 
from django.utils.safestring import mark_safe   #etminan be jango az amn bodan



# @register.filter(name='markdown')     #filter ekhtesasi khodemon
# def markdown_format(text):
#     return mark_safe(markdown.markdown(text))


@register.filter(name='markdown')     #filter ekhtesasi khodemon
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
