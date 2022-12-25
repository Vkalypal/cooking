import requests
from bs4 import BeautifulSoup
from time import sleep
import pymongo


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


# подключаемся к базе
db_client = pymongo.MongoClient('mongodb://localhost:27017/')

# подключаемся к бд, если нет то создаётся
current_db = db_client['cooking']

# подключаемся к коллекции, аналог таблицы из реляционных бд
collection = current_db['recipes']


def get_url():
    print('dfsdf')
    for count in range(131, 141):
        url = f'https://eda.ru/recepty?page={count}'

        res = requests.get(url, headers=headers)

        # Сохраняем основную страницу
        src = res.text
        # with open('index.html', 'w', encoding='utf-8') as file:
        #     file.write(src)
        # with open('index.html', encoding='utf-8') as file:
        #     src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        # Блок с обьявленем
        all_recipes = soup.find_all('div', class_='emotion-m0u77r')
        for item in all_recipes:
            href = 'https://eda.ru' + item.find('a', class_='emotion-18hxz5k').get('href')
            yield href


def array():
    for recipes in get_url():
        res = requests.get(recipes, headers=headers)
        sleep(3) # Пауза 3 секунды
        soup = BeautifulSoup(res.text, 'lxml')
        result = soup.find('div', class_='emotion-2k9cfu')
        #print(result)

        name = result.find('h1', class_='emotion-gl52ge').text
        ingredients = result.find_all('span', itemprop='recipeIngredient')
        for ing in range(len(ingredients)):
            ingredients[ing] = ingredients[ing].text
        #strip() Удаление пробелов слева справа
        href = recipes
        #print(f'Название блюда: {name}\nИнгридиенты: {str(ingridients)}\nСсылка: {href}')
        #yield name, str(ingridients), href


        recipe = {
            'name': name,
            'ingredients': ingredients,
            'href': href
        }

        # добавляем объект
        ins_result = collection.insert_one(recipe)
        print(ins_result) # ид вставленного объекта

# вывод всех документов в коллекции
# for recpt in collection.find():
#     print(recpt)


array()