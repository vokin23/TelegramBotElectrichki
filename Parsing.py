from bs4 import BeautifulSoup
import requests
import json


def get_data(url: str = 'https://www.tutu.ru/rasp.php?st1=45807&st2=50607&date=tomorrow') -> dict[str, dict]:
    """
        Принимаемые аргументы:
            - url: ссылка на страницу. Значение по умолчанию ссылка на поезда с туту.ру, которую ты мне скинул

        Возвращаемое значение:
            - словарь всех поездов с их данными
                - Ключи словаря - порядковые номера поездов
                - Значения словаря - словари с данными о поезде
                    - Ключи словаря с данными:
                        - start_time - время отправления
                        - end_time - время прибытия
                        - movement - режим движения
                        - time_in_road - время в пути
                        - way - пункт отправления -> путь назначения
                    - Значения словаря с данными - сами данные
            - пример вывода резуьтата работы функции:
                {
                    "1": {
                        "start_time": "04:00",
                        "end_time": "06:34",
                        "movement": "ежедневно",
                        "time_in_road": "1 ч 54 м",
                        "way": "Москва Ярославская → Александров-1"
                    },
                    "2": {
                        "start_time": "06:35",
                        "end_time": "08:03",
                        "movement": "ежедневно",
                        "time_in_road": "1 ч 28 м",
                        "way": "Москва Ярославская → Александров-1"
                    },
                    "3": {
                        ...
                    },
                    ...
                }

        Работа функции:
            - table. На полученной странице находим таблицу. Тип данных строка (str) в виде HTML-кода
            - rows. В полученной таблице находим все теги tr, в которых лежат данные о поездах. Тип данных - список (list)
            - for train_number (порядковый номер поезда, который будет ключем в JSON-файле), row (сам поезд, а точнее данные о нём) in enumerate(rows, start=1).
                Цикл, который перебирает все данные о поездах, собирает их в словарь. Как только весь словарь собран - отправляет его в return.
            - функция "Кодер Крутой".replace("Крутой", "Долбоёб") Заменяет в строке "Кодер Крутой" слово "Крутой" на слово "Долбоёб"
    """
    result = {}

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find('tbody', class_='desktop__timetable__3wEtY')
    rows = table.find_all('tr')

    for train_number, row in enumerate(rows, start=1):
        start_time, end_time, movement, time_in_road, way = [i.text for i in row.find_all('td')[:5]]

        result[train_number] = {
            "start_time": start_time,
            "end_time": end_time,
            "movement": movement,
            "time_in_road": time_in_road.replace("\u202f", " ").replace("\xa0", " ").replace("\u202f", " "),
            "way": way.replace("\xa0", " ").replace("\u2002", " ")
        }

    return result


def write_to_json(data: dict = get_data()):
    """
        Принимаемые аргументы:
            - data: словарь с данными, которые надо закинуть в JSON-файл

        Возвращаемые значения:
            - Нихуя не возвращает

        Работа функции:
            - json.dump(data, file): метод библиотеки JSON, позволяющий записать данные в JSON файл.
                - data: данные, которые надо записать
                - file: файл, в который надо записать
    """
    with open("tutu.json", "w") as file:
        json.dump(data, file)
        print("Все данные добавились")


def get_train(train_number: str) -> dict[str]:
    """
        Принимаемые аргументы:
            - train_number: номер поезда в JSON-файле. Тип данных -  строка

        Возвращаемые значения:
            - Словарь с данными о конкретном поезде. Тип данных - словарь

        Работа функции:
            - json.load(file): метод библиотеки JSON, позволяющий считать данные из JSON-файла.
                - file: файл, из которого надо считать данные.
    """
    with open("tutu.json", 'r', encoding='utf-8') as file:
        trains = json.load(file)

    return trains[train_number].items()

def main():
    get_data()
    write_to_json()