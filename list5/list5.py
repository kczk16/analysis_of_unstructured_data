from geotext import GeoText
from bs4 import BeautifulSoup
import wikipedia
import re

with open('around.txt', 'r') as f:
    book = f.readlines()[78:]

keywords = ["arriv", "come", "came", "by boat", "by train", "by ship", "by steamer", "by rail", "visit", "reach",
            "Reach", "Left", "stop", "enter", "leav", "left", "get to", "stay", "exit", "depart", "return", "back to",
            "journey", "start"]


def get_context(line_index):
    if line_index == 0:
        return book[line_index:line_index+1]

    if line_index >= 8229:
        return book[line_index-2:line_index]

    return book[line_index-2:line_index+1]


def look_for_place(line, lineindex):
    line = _replace_city_names(line)
    # line = line.split(" ")
    # line[0] = line[0].lower() #wyniesc do funkcji zeby robilo places na calym zdaniu + na zdaniu z lower i set
    # line = " ".join(line)
    places = GeoText(line)
    context = get_context(lineindex)
    for key in keywords:
        for sentence in context:
            if key in sentence:
                return places


def search_for_places(book):
    cities = {}
    for index, line in enumerate(book):
        places = look_for_place(line, index)
        if places:
            for i in range(len(places.cities)):
                if places.cities[i] in cities.keys():
                    cities[places.cities[i]] += 1
                else:
                    for i in range(len(places.cities)):
                        cities[places.cities[i]] = 1
    return {key: value for key, value in cities.items()}


def _replace_city_names(line):
    changes = _get_changed_cities()
    for pair, val in changes.items():
        for i in range(len(pair)-1):
            if pair[i] in line and pair[i] != "York":
                line = line.replace(pair[i], val[0])
                print(pair, i)
                print('pair', pair[i])
                print('val', val[0])
    return line


def _get_changed_cities():
    changed_cities = wikipedia.page("List_of_city_name_changes")
    soup = BeautifulSoup(changed_cities.html(), "html.parser")
    changed_cities_soup = [c for c in soup.find_all("ul")]
    change = []
    for i in changed_cities_soup:
        for j in i.find_all("li"):
            change.append(j.get_text())
    index = change.index('Alexandria Ariana → Herat')
    index2 = change.index('List of administrative division name changes')
    change = change[index:index2]
    cities = [pair.split('→') for pair in change]
    to_change = {}
    for city in cities:
        to_change[tuple([_clean_text(city[j].strip()) for j in range(len(city)-1)])] = [_clean_text(city[-1].strip())]
    return to_change


def _clean_text(text):
    pattern = "\([[0-9]+\)+|\[[[0-9]+\]"
    text = re.sub(pattern, '', text)
    return text.strip()


