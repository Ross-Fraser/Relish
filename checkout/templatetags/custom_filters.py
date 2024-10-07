from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    try:
        return float(value) * int(arg)
    except (ValueError, TypeError):
        return None

@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    return price * quantity
