# -----------------------------------------------------
# parses data from resh.edu.ru
# 
# (C) 2021 Visstudii, Saratov, Russia
# contact: dungeongachi6hotloads@gmail.com
# -----------------------------------------------------


import requests
from requests.sessions import Session
import cache
import json
from bs4 import BeautifulSoup as bs
from threading import Thread


class Parser():
    MAIN_URL = "https://resh.edu.ru"

    #Dictionaries
    SUBJECTS = {}
    LESSONS = {}
    TASKS = {}
    ANSWERS = {}
    
    #Lambdas
    ANSWERS_REQUEST = lambda task: Parser.MAIN_URL + "/tests/%s/get-answers" % task
    LESSON_HREF = lambda lesson: Parser.MAIN_URL + lesson + "train"
    PAGE_REQUEST = lambda subject, grade, page: \
        "%s/subject/%s/%s/ajax?page=%s" % (Parser.MAIN_URL,
                                            subject,
                                            grade,
                                            page)
    STRIP = lambda Url: int(str.strip(Url, "/subject/lesson/"))
    
    def parse_subjects(self):
        # Parses all subjects
        with requests.Session() as session:
            request = session.post(Parser.MAIN_URL  + "/subject")
            soup = bs(request.text, "html.parser")
            for subjectCell in soup.find_all("a", "subject-cell"):
                Parser.SUBJECTS[subjectCell.
                select_one("span").string] = Parser.STRIP(subjectCell.get("href"))

    def parse_lessons(self, subject, grade):
        # Parses all lessons
        with requests.Session() as session:
            page = 1
            lesson = 1
            while page is not False:
                request = session.get(Parser.PAGE_REQUEST(subject, grade, page))
                returnedHtml = request.json()["html"]
                soup = bs(returnedHtml, "html.parser")
                for lessonBlock in soup.find_all("a", "lesson-block"):
                    self.LESSONS[lesson] = Parser.LESSON_HREF(lessonBlock["href"])
                    lesson += 1
                page = request.json()["nextPage"]
    
    def parse_tasks(self, lesson):
        # Parses all tasks
        with requests.Session() as session:
            task = 1

            request = session.get(self.LESSONS[lesson])
            returnedHtml = request.text
            soup = bs(returnedHtml, "html.parser")
            for taskBlock in soup.find_all("li", "test__task-num"):
                self.TASKS[task] = Parser.STRIP(taskBlock["data-test-id"])
                task += 1

    def parse_answers(self, subject, grade, lesson):
        # Parses all answers
        with requests.Session() as session:
            for task in self.TASKS.values():
                request = session.post(Parser.ANSWERS_REQUEST(task),
                headers={"X-Requested-With": "XMLHttpRequest"})
                self.ANSWERS[task] = request.iter_lines()[0]


class FileManager():
    
    def write_json(self, message, subject, grade, lesson, task):
        with open("%s %s класс - урок №%s задание №%s.json" %
        (subject, grade, lesson, task), 
        "w", encoding="utf-8") as file:
            json.dump(message, file, indent=4, ensure_ascii=False)


class CacheManager():
    pass