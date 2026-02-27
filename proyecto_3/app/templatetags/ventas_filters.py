from django import template

register = template.Library()

@register.filter
def precio_co(value):
    """Formatea un número como precio colombiano: 1.234.567"""
    try:
        return '{:,.0f}'.format(float(value)).replace(',', '.')
    except (ValueError, TypeError):
        return value
