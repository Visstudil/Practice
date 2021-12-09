from bs4.element import *
import requests
from bs4 import BeautifulSoup as bs
import json

class CorrectAnswers:

    MAIN_URL = "https://resh.edu.ru"
    LESSON_URL = "https://resh.edu.ru/subject/lesson/{0}/train/"
    TEST_URL = "https://resh.edu.ru/subject/lesson/2933/train/{0}"
    GET_ANSWERS_URL = "https://resh.edu.ru/tests/{0}/get-answers"
    SUBJECTS = {}
    COOKIES = {"PHPSESSID": ""}
    HTML = "index.html"
    HEADERS = {"User-Agent": "Chrome/94.0.4606.71",
            "Accept" : "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "XMLHttpRequest"}

    INTERACTION_TYPES = {
        "word_place":    "gap_match_text",
        "word_input":    "text_entry",
        "association":   "two_sets_association",
        "checkbox":      "multiple_choice",
        "radiobutton":   "single_choice",
        "color":         "gap_match_color",
        "table":         "gap_match_table",
        "inline_choice": "inline_choice",
        "crossword":     "interactive_crossword",
        "rebus":         "interactive_rebus",
        "imagetext":     "gap_match_image_text",
        "matrix":        "gap_match_matrix",
        "underline":     "gap_match_underline"
    }
    PAYLOAD = {"answers": "{"}

    req = requests.get(MAIN_URL)
    soup = bs(req.text, "html.parser")


    def __init__(self):
        for link in self.soup.find_all("a"):  # Fill up SUBJECTS
            if "/subject/" in link.get("href"):
                q = requests.get(self.MAIN_URL + link.get("href"))
                subjectName = bs(q.text, "html.parser").find_all("h1", {"class": "content-title"})[0].getText().lower()
                subjectID = link.get("href").strip("/subject")
                if subjectID != "":
                    self.SUBJECTS[subjectName] =  subjectID
    

    def interaction_type(self, url, id):
        html = requests.get(url).text
        soup = bs(html, "html.parser")
        task = bs(str(soup.find_all(attrs={"data-test-id": id})), "html.parser")
        for key, value in self.INTERACTION_TYPES.items():
            element = task.find_all(attrs={"data-interaction-type": value})
            if element != []:
                return key
        pass


    def get_lesson_id(self, sbj, cls, lsn):
        output = []
        page = 1
        subjectURL = "{}/subject/{}/{}".format(self.MAIN_URL, self.SUBJECTS[sbj], cls)

        while True:
            html = requests.post(subjectURL + "/ajax?page={}".format(page), headers=self.HEADERS).json()["html"]
            lessonBlocks = bs(html, "html.parser").find_all("a", {"class": "lesson-block"})
            for link in lessonBlocks:
                output.append(str(link.get("href")).strip("/subject/lesson"))
            page += 1

            if page > 4:
                break
        
        return output[lsn - 1]


    def get_answer_by_id(self, id, lesson, subject, class_, lessonID, task):
        self.HEADERS["Referer"] = "https://resh.edu.ru/subject/lesson/{0}/train/".format(lesson)
        out = []
        with requests.Session() as session:
            r = session.post(r"https://resh.edu.ru/", headers=self.HEADERS)
            self.COOKIES["PHPSESSID"] = r.cookies["PHPSESSID"]
            answerRequest = session.post("https://resh.edu.ru/tests/{0}/get-answers".format(id),
            headers=self.HEADERS, cookies=self.COOKIES)

            for msg in answerRequest.iter_lines():
                out.append(json.loads(msg))
            with open("{0}-{1} класс-{2} урок-{3} задание.json".format(subject, class_, lesson, task), "w", encoding="utf-8") as f:
                json.dump(out, f, indent=4, ensure_ascii=False)
                print(self.interaction_type("https://resh.edu.ru/subject/lesson/{0}/train/{1}".format(lessonID, id), id))
                print(msg)
            return out
    

    def parse_answers(self, lesson_, subject_, class_):
        testIDs = []
        lessonID = self.get_lesson_id(subject_, class_, lesson_)
        req = requests.get("https://resh.edu.ru/subject/lesson/{0}/train/".format(lessonID))
        soup = bs(req.text, "html.parser")
        
        tests = soup.find_all("li", {"class": "test__task-num"})
        for test in tests:
            testIDs.append(test["data-test-id"])
        i = 1
        for id in testIDs:
            json = self.get_answer_by_id(id, lesson_, subject_, class_, lessonID, i)
            print("JSON = {}".format(str(json)))
            self.PAYLOAD["answers"] = self.PAYLOAD["answers"] +'"{0}":{{"{1}":{2}}}'.format(id, ("RESPONCE1_1" if "RESPONCE1_1" in str(json) else "RESPONCE1"), 0)
            i += 1
        with requests.Session() as session:
            self.PAYLOAD["answers"] = self.PAYLOAD["answers"] + "}"
            print("\n\nPAYLOAD\n", self.PAYLOAD["answers"])
            print(session.post("https://resh.edu.ru/subject/lesson/1548/train/result/", headers=self.HEADERS, cookies=self.COOKIES, data=self.PAYLOAD).text)

chtml = CorrectAnswers()

subject = input("Введите название предмета: ").lower()
class_ = int(input("Введите класс: "))
lesson = int(input("Введите номер урока: "))
chtml.parse_answers(lesson, subject, class_)