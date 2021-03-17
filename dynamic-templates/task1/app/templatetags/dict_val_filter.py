from django import template

register = template.Library()


@register.filter
def dict_val(dict: dict, key: str):
    if key == 'Год':
        return dict.get(key)
    else:
        if  dict.get(key) == '':
            return 0.0

        return float(dict.get(key)) # для того что бы сравнение работало

