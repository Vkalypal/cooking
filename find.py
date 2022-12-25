import pymongo, xlsxwriter
from collections import Counter


# # подключаемся к базе
# db_client = pymongo.MongoClient('mongodb://localhost:27017/')
# # подключаемся к бд, если нет то создаётся
# current_db = db_client['cooking']
# # подключаемся к коллекции, аналог таблицы из реляционных бд
# collection = current_db['recipes']

# подключаемся к базе
db_client = pymongo.MongoClient('mongodb://localhost:27017/')
# подключаемся к бд, если нет то создаётся
current_db = db_client['test']
# подключаемся к коллекции, аналог таблицы из реляционных бд
collection = current_db['recipe']

# query = []
# query = input('Какие продукты у вас есть?')
# print(query)


def get_name():
    i = 0
    a = []
    for name in collection.find():
        a.append(name['name'])

    for name in a:
        i += 1
        print(f'{i} {name}')

def ingrd_base():
    i = 0
    a = []
    for recipe in collection.find():
        a.append(recipe['ingredients'])

    k = set(sum(a, [])) # объединили список списков

    for ing in k:
        i += 1
        print(f'{i} {ing}')

    return k

def search_ing(k):
    i = 0
    for ing in k:
        if ing.lower().find('сыр') != -1:
            i += 1
            print(f'{i} {ing}')

def search_dublicate():
    a = []
    for name in collection.find():
        a.append(name['name'])
    result = Counter(a)
    print(result)

#ing = ['Пшеничная мука', 'Молоко', 'Растительное масло', 'Сухие дрожжи', 'Сахар', 'Соль', 'Яичные желтки', 'Сливочное масло']
# точное совпадение рецепта
# for recipe in collection.find({'$and': [{'ingredients': {'$size': len(ing)}}, {'ingredients': {'$all': ing}}]}):
#     print(type(recipe))
#     print(f'Вы можете приготовить: {recipe["name"]}. Подробный рецепт по ссылке: {recipe["href"]}')

# ing = ['Вишня', 'Вода', 'Сахар']
# for recipe in collection.find({'ingredients': {'$in': ing}}): #, {'_id': 0, 'name': 1, 'href': 1}):
#     print(len(recipe['ingredients']))
#     print(f'Вы можете приготовить: {recipe["name"]}. Подробный рецепт по ссылке: {recipe["href"]}')

def writer(parametr):
    book = xlsxwriter.Workbook(r'ingredients.xlsx') # Файл таблицы
    page = book.add_worksheet('Ингредиенты') # Название листа

    row = 0
    column = 0
    # Ширина колонок
    page.set_column('A:A', 50)

    for item in parametr:
        page.write(row, column, item)
        # page.write(row, column + 1, item[1])
        # page.write(row, column + 2, item[2])
        row = row + 1

    book.close()

def change():
    d = {
        'Российский сыр': 'Сыр',
        'Тертый сыр пармезан ': 'Сыр',
        'Куриное яйцо': 'Яйца',
        'Сливки 20%-ные': 'Сливки'
    }

    for key in d:
        collection.update_many({'ingredients': key}, {'$set': {'ingredients.$': d[key]}})
    for recipe in collection.find():
        print(recipe)
    # for recipe in collection.find({'ingredients': {'$in': ing}}, {'_id': 1}):
        # print(recipe.items())
        # print(collection.index_information())
        # collection.update_one({'_id': '63a427e1908501a6d22e96d3'}, {'$pullAll': {'ingredients': ing}})
        # print('+')
#search_ing(ingrd_base())
#ingrd_base() # вывод всех ингредиентов
#search_dublicate()
#get_name()
#writer(ingrd_base())
change()