from django.shortcuts import render
from django.http import Http404


DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def recipe_view(request, dish_name):
    # Пытаемся найти рецепт в DATA
    if dish_name in DATA:
        recipe = DATA[dish_name]
        servings = request.GET.get('servings')

        # расчет ингридиетов согласно колличества персон
        if servings is not None:
            DATA_NEW = {}
            for key, valuems in recipe.items():
                DATA_NEW[key] = valuems * int(servings)
            recipe = DATA_NEW.copy()

        return render(request, 'calculator/index.html', context={'recipe': recipe})
    else:
        # Если рецепта нет - ошибка 404
        raise Http404("Такого рецепта не знаю :(")
    
# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }
