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
    LESSONS = {}

    def __init__(self):
        # Parse the school subjects page
        request = requests.get(Parser.MAIN_URL + Parser.SUBJECT_SUFFIX)
        soup = bs(request.text, "html.parser")

        # Fill up the dictionary
        for subjectCell in soup.find_all("a", "subject-cell"):
            Parser.SUBJECTS[subjectCell.
            select_one("span").string] = subjectCell.get("href")

    def parse_lessons_links(self, _subject, _class):
            page = 1
            lessonNumber = 1
            while page is not False:
                request = requests.post(Parser.MAIN_URL 
                                        + str(_subject)
                                        + str(_class)
                                        + Parser.PAGE_REQUEST
                                        + str(page))

                returnedHtml = request.json()["html"]

                soup = bs(returnedHtml, "html.parser")
                for a in soup.find_all("a", "lesson-block"):
                    self.LESSONS[lessonNumber] = self.MAIN_URL + a["href"]
                    lessonNumber += 1

                page = request.json()["nextPage"]


    def parse_answers(self):
        pass

    def write_json(self):
        pass


initialize = Thread(target=Parser.__init__(Parser))
initialize.start()
print(Parser.SUBJECTS)

parser = Parser()
selectedSubject = str(input("subject >>>"))
selectedClass = int(input("class >>>"))
selectedLesson = int(input("lesson >>>"))

parser.parse_lessons_links(Parser.SUBJECTS[selectedSubject], selectedClass)
print(Parser.LESSONS[int(selectedLesson)])
