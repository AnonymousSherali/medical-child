from decimal import Decimal, InvalidOperation

from django import template
from django.utils.formats import number_format

register = template.Library()


@register.filter
def num(value):
    """Decimal qiymatni ortiqcha nollarsiz, lokal formatda chiqaradi.

    DecimalField 27.360 ni "27,360" deb ko'rsatadi — o'zbek lokalida bu yigirma
    yetti mingdek o'qiladi. Filtr natijasi: "27,36"; 35.00 -> "35".
    """
    if value is None or value == '':
        return ''
    try:
        number = Decimal(str(value)).normalize()
    except (InvalidOperation, ValueError):
        return value
    exponent = number.as_tuple().exponent
    places = -exponent if exponent < 0 else 0
    return number_format(number, decimal_pos=places)
