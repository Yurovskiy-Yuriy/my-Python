from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator


import csv

def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    
    stations = []  # Список для хранения данных о станциях

    # чтение в словарь с DictReader:
    with open('data-398-2018-08-30.csv', encoding='utf-8') as f:
        reader =csv.DictReader(f) # теперь все данные это словарь { }

        for row in reader:
            stations.append({
                'Name': row['Name'],
                'Street': row['Street'],
                'District': row['District'],
            })            
    
    # Получаем номер страницы из GET-параметра (по умолчанию 1)
    page_number = int(request.GET.get("page", 1))

    # Создаём пагинатор: все данные, по 10 элементов на страницу
    paginator = Paginator(stations, 10)

    # Получаем объект страницы (автоматически конвертирует page_number в int)
    page = paginator.get_page(page_number)
    
    # передаем список в контекст
    context = {'bus_stations': page}
    
    return render(request, 'stations/index.html', context)

