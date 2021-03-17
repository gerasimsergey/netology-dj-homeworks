import csv, os

from django.shortcuts import render

from csv import DictReader

# !!! правильное обращение к тому что прописано в  settings !!!
from django.conf import settings


def load_inflation_data():
    with open('inflation_russia.csv', newline='') as csvfile:
        header = ''
        rows = []
        reader = csv.reader(csvfile)
        for row in reader:
            if reader.line_num == 1:
                header = row[0].split(";")
                break

    with open('inflation_russia.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if reader.line_num == 1:
                continue

            rows.append(row)

    return header, rows

def inflation_view(request):
    template_name = 'inflation.html'
    header, data = load_inflation_data()
    context = {
        'header': header,
        'data': data,
    }

    return render(request, template_name, context)
