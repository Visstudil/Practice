# -----------------------------------------------------
# Parses data from resh.edu.ru
# 
# (C) 2021 Visstudii, Saratov, Russia
# contact: dungeongachi6hotloads@gmail.com
# -----------------------------------------------------


import json
import os
import requests
from bs4 import BeautifulSoup as bs

class Page():
    subjects = {}
    lessons = []
    tasks = []
    answers = []
    subject = ""
    grade = 0
    lesson = 0

    def __str__(self):
        return (self.subject, "%i класс" % self.grade, "%i урок" % self.lesson)


class Parser():
    MAIN_URL = "https://resh.edu.ru"

    #Lambdas
    ANSWERS_REQUEST = lambda task: Parser.MAIN_URL + "/tests/%s/get-answers" % task
    LESSON_HREF = lambda lesson: Parser.MAIN_URL + lesson + "train"
    PAGE_REQUEST = lambda subject, grade, page: \
        "%s/subject/%s/%s/ajax?page=%s" % (Parser.MAIN_URL,
                                            subject,
                                            grade,
                                            page)
    STRIP = lambda Url: int(str.strip(Url, "/subject/lesson/"))

    def reset(self, subject, grade, lesson):
        self.page = Page()
        self.page.subject = subject
        self.page.grade = grade
        self.page.lesson = lesson
    
    def parse_subjects(self):
        # Parses all subjects
        with requests.Session() as session:
            request = session.post(Parser.MAIN_URL  + "/subject/")
            soup = bs(request.content, "html.parser")
            for subjectCell in soup.find_all("a", "subject-cell"):
                self.page.subjects[subjectCell.select_one("span").string] = Parser.STRIP(subjectCell.get("href"))


    def parse_lessons(self):
        # Parses all lessons
        with requests.Session() as session:
            page = 1
            lesson = 1
            while page is not False:
                request = session.get(Parser.PAGE_REQUEST(self.page.subjects[self.page.subject], self.page.grade, page))
                returnedHtml = request.json()["html"]
                soup = bs(returnedHtml, "html.parser")
                for lessonBlock in soup.find_all("a", "lesson-block"):
                    self.page.lessons.append(Parser.LESSON_HREF(lessonBlock["href"]))
                    lesson += 1
                page = request.json()["nextPage"]
    

    def parse_tasks(self):
        # Parses all tasks
        with requests.Session() as session:
            task = 1
            request = session.get(self.page.lessons[self.page.lesson-1])
            returnedHtml = request.text
            soup = bs(returnedHtml, "html.parser")
            for taskBlock in soup.find_all("li", "test__task-num"):
                self.page.tasks.append(Parser.STRIP(taskBlock["data-test-id"]))
                task += 1


    def parse_answers(self):
        # Parses all answers
        with requests.Session() as session:
            for task in self.page.tasks:
                request = session.post(Parser.ANSWERS_REQUEST(task),
                headers={"X-Requested-With": "XMLHttpRequest"})
                self.page.answers.append(next(request.iter_lines()).decode("utf-8"))


class PageManager():
    parser: Parser
    
    def make_page(self, subject, grade, lesson):
        self.parser.reset(subject, grade, lesson)
        self.parser.parse_subjects()
        self.parser.parse_lessons()
        self.parser.parse_tasks()
        self.parser.parse_answers()


class CacheManager():
    page: Page
    path = ""

    def __init__(self):
        self.path = os.path.join(os.getcwd(), "Cache")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def save_page(self):
        path = self.path
        for argument in self.page.__str__():
            path = os.path.join(path, str(argument))
            if not os.path.exists(path): os.mkdir(path)
        fileName = "%s-%s класс-%s урок.json" % self.page.__str__()
        with open(os.path.join(path, fileName), "w", encoding="utf-8") as f:
            json.dump(self.page.answers, f, ensure_ascii=False, indent=4)

    def search_page(self):
        pass

    def arcive(self):
        pass
    
    def cache(self):
        pass


class Main():
    parser = Parser()
    cacheManager = CacheManager()
    pageManager = PageManager()
    pageManager.parser = parser
    while True:
        subject = input("Название предмета >>> ")
        grade = int(input("Класс >>> "))
        lesson = int(input("Урок >>> "))
        pageManager.make_page(subject, grade, lesson)
        cacheManager.page = parser.page
        cacheManager.save_page()
