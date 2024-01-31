from django import template
import datetime

register = template.Library()

@register.filter
def runtime_to_hours(value):
    h=value//60
    m=value%60
    return f"{h}h{m}min"

@register.filter
def release_date_to_year(value):
    return value.year

@register.filter
def int_to_money(value):
    return "${:,}".format(value)

@register.filter
def cast_comma(value):
    return value[:-2]