from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib import parse
from csv import DictReader

# !!! правильное обращение к тому что прописано в  settings !!!
from django.conf import settings


def index(request):
    return redirect(reverse(bus_stations))


def get_bus_station_data():
    list = []
    with open(settings.BUS_STATION_CSV, newline='', encoding='cp1251') as csvfile:
        reader = DictReader(csvfile)
        for row in reader:
            list.append(
                {'Name': row['Name'], 'Street': row['Street'], 'District': row['District']}
            )

    return list

# можно и в bus_stations, но так вроде не будет читать с диска постояно
POST = get_bus_station_data()


def make_page_url(page_number):
    if page_number == None:
        return
    bus_stations_page_url = reverse('bus_stations')
    bus_stations_page_url = bus_stations_page_url + "?%s"
    params = parse.urlencode({'page': page_number})
    return bus_stations_page_url % params


def bus_stations(request):
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    paginator = Paginator(POST, settings.APP_LINE_PER_PAGE)
    page = paginator.get_page(current_page)


    if page.has_next():
        next_number = page.next_page_number()
    else:
        next_number = None

    next_page_url = make_page_url(next_number)

    if page.has_previous():
        prev_number = page.previous_page_number()
    else:
        prev_number = None

    if prev_number == None:
        prev_page_url = None
    else:
        prev_page_url = make_page_url(prev_number)

    return render(request, 'index.html', context={
        'bus_stations': page.object_list,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
