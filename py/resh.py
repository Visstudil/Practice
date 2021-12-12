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

    #Urls:
    MAIN_URL = "https://resh.edu.ru"
    SUBJECT_SUFFIX = "/subject"
    PAGE_REQUEST = lambda _subject, _class, _page: \
        "%s/subject/%s/%s/ajax?page=%s" % (Parser.MAIN_URL,
                                            _subject,
                                            _class,
                                            _page)
    STRIP = lambda Url: int(str.strip(Url, "/subject/lesson/"))
    LESSON_WRAP = lambda lesson: \
        Parser.MAIN_URL + lesson + "train"

    #Dictionaries:
    SUBJECTS = {}
    LESSONS = {}
    TASKS = {}

    def __init__(self):
        # Parse the school subjects page and write links to dictionary:
        request = requests.get(Parser.MAIN_URL + Parser.SUBJECT_SUFFIX)
        soup = bs(request.text, "html.parser")
        for subjectCell in soup.find_all("a", "subject-cell"):
            Parser.SUBJECTS[subjectCell.
            select_one("span").string] = Parser.STRIP(subjectCell.get("href"))

    def parse_lessons_links(self, _subject, _class):
        pageNumber = 1
        lessonNumber = 1

        while pageNumber is not False:
            request = requests.get(Parser.PAGE_REQUEST(_subject,
                                                        _class,
                                                        pageNumber))
            returnedHtml = request.json()["html"]
            soup = bs(returnedHtml, "html.parser")
            for lessonBlock in soup.find_all("a", "lesson-block"):
                self.LESSONS[lessonNumber] = Parser.LESSON_WRAP(lessonBlock["href"])
                lessonNumber += 1
            pageNumber = request.json()["nextPage"]
    
    def parse_tasks_links(self, _lesson):
        taskNumber = 1

        request = requests.get(self.LESSONS[_lesson])
        returnedHtml = request.text
        soup = bs(returnedHtml, "html.parser")
        for taskBlock in soup.find_all("li", "test__task-num"):
            self.TASKS[taskNumber] = Parser.STRIP(taskBlock["data-test-id"])
            taskNumber += 1

    def parse_answers(self):
        pass

    def write_json(self):
        pass

    def cache(self):
        pass

    def __del__(self):
        pass


parser = Parser()

initialize = Thread(target=parser.__init__())
initialize.start()
print(parser.SUBJECTS)

selectedSubject = str(input("subject >>>"))
selectedClass = int(input("class >>>"))
selectedLesson = int(input("lesson >>>"))

parser.parse_lessons_links(Parser.SUBJECTS[selectedSubject], selectedClass)
print(Parser.LESSONS)
parser.parse_tasks_links(selectedLesson)
print(Parser.TASKS)
