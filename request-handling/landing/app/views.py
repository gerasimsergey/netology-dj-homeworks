from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся

counter_show = Counter()
counter_click = Counter()

def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    param = request.GET.get('from-landing', '')
    if param == 'original':
        counter_click.update(['original'])
    if param == 'test':
        counter_click.update(['test'])
    else:
        counter_click.update(['direct'])

    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов

    param = request.GET.get('ab-test-arg', '')

    if param == 'test':
        counter_show.update(['test'])
        return render(request, 'landing_alternate.html')

    if param == 'original':
        counter_show.update(['original'])
        return render(request, 'landing.html')

    if param == '':  # проблема не передали
        counter_show.update(['not_param']);
        render(request, 'index.html')


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    test_show = int(counter_show['test'])
    test_click = int(counter_click['test'])
    if test_show > 0:
        test_conversion = (test_click / test_show * 100)
    else:
        test_conversion = 'Тесты не проводились, показов: 0'

    original_show = int(counter_show['original'])
    original_click = int(counter_click['test'])

    if original_show > 0:
        original_conversion = (original_click / original_show * 100)
    original_conversion = 'Тесты не проводились, показов: 0'

    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
