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



@register.filter
def color_filter(dict: dict, key: str):
    if key == 'Суммарная':
        return 'gray'
    elif key == 'Год':
        return 'white'

    else:
        value = dict.get(key)

        if value == '':
            value = 0.0
        else:
            value = float(value)

        if value < 0:
            return 'green'

        if  value <= 1:
            return 'white'

        if value > 1 and value <= 2:
            return 'pink'

        if value > 2 and value < 5:
            return '#f16969'

        if  value > 5:
            return '#ff0000'

        else:
            return 'white'




