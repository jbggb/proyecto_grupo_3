from django import template

register = template.Library()

@register.filter
def precio_co(value):
    try:
        return '{:,.0f}'.format(float(value)).replace(',', '.')
    except:
        return value