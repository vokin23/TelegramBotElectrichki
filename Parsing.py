from bs4 import BeautifulSoup
import requests
import json


def get_data(url: str = 'https://www.tutu.ru/rasp.php?st1=45807&st2=50607&date=tomorrow') -> dict[str, dict]:

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

    with open("tutu.json", "w") as file:
        json.dump(data, file)
        print("Все данные добавились")


def get_train(train_number: str) -> dict[str]:

    with open("tutu.json", 'r', encoding='utf-8') as file:
        trains = json.load(file)

    return trains[train_number].items()

def main():
    get_data()
    write_to_json()