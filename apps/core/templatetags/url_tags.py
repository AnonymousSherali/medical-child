from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def querystring_without(context, *keys):
    """Joriy GET parametrlarini qaytaradi, `keys` dagilarini olib tashlab.

    Sahifalashda ishlatiladi: `?page=2{% querystring_without 'page' %}` —
    aks holda URL'da ikkita `page` paydo bo'lib, filtr buziladi.
    """
    request = context.get('request')
    if request is None:
        return ''
    params = request.GET.copy()
    for key in keys:
        params.pop(key, None)
    encoded = params.urlencode()
    return f'&{encoded}' if encoded else ''
