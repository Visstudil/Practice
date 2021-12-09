import json
from bs4 import BeautifulSoup as bs
import requests

def print_by_type(type, json_, taskURL):
    with requests.Session() as s:
        soup = bs(s.get(taskURL).text, "html.parser")
        task = soup.find_all("input", {"class": "interaction-choice tests-chk"})
        with open(json_, "r") as j:
            print(json.loads(j)["value"])

print_by_type("checkbox", "История-8 класс-13 урок-4 задание.json", "https://resh.edu.ru/subject/lesson/1577/train/#183586")