# -----------------------------------------------------
# parses data from resh.edu.ru
# 
# (C) 2021 Visstudii, Saratov, Russia
# contact: dungeongachi6hotloads@gmail.com
# -----------------------------------------------------


import requests
import json
from bs4 import BeautifulSoup as bs
from threading import Thread


class Parser():


    MAIN_URL = "https://resh.edu.ru"
    SUBJECT_SUFFIX = "/subject/"
    PAGE_REQUEST = "/ajax?page="

    SUBJECTS = {}
    LESSONS = {}  # ToDo Номер урока - его адрес

    def __init__(self):
        # Parse the school subjects page
        request = requests.get(Parser.MAIN_URL + Parser.SUBJECT_SUFFIX)
        soup = bs(request.text, "html.parser")

        # Fill up the dictionary
        for subjectCell in soup.find_all("a", "subject-cell"):
            Parser.SUBJECTS[subjectCell.
            select_one("span").string] = subjectCell.get("href")

    def parse_lessons_id_list(self, subjectID, classNumber):
            page = 1
            while page is not False:
                request = requests.post(Parser.MAIN_URL 
                                        + subjectID
                                        + classNumber
                                        + Parser.PAGE_REQUEST
                                        + str(page))
                page = request.json()["nextPage"]
                print(request.json()["html"])

    def parse_answers(self):
        pass

    def write_json(self):
        pass


initialize = Thread(target=Parser.__init__(Parser))
initialize.start()
print(Parser.SUBJECTS)

parser = Parser()
subject_ = str(input("subject >>>"))
class_ = str(input("class >>>"))
parser.parse_lessons_id_list(Parser.SUBJECTS[subject_], class_)
