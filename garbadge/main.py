import requests
import json
from bs4 import BeautifulSoup as bs
import time

SUBJECTS = {}
COOKIES = {"PHPSESSID": ""}
HTML = "index.html"
HEADERS = {"User-Agent": "Chrome/94.0.4606.71",
            "Accept" : "*/*",
            "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With": "XMLHttpRequest"}
mainURL = "https://resh.edu.ru"


req = requests.get(mainURL)
soup = bs(req.text, "html.parser")


def setup():
    for link in soup.find_all("a"):  # Fill up SUBJECTS
        if "/subject/" in link.get("href"):
            print(req.request.headers)
            q = requests.get(mainURL + link.get("href"))
            subjectName = bs(q.text, "html.parser").find_all("h1", {"class": "content-title"})[0].getText()
            subjectID = link.get("href").strip("/subject")
            if subjectID != "":
                SUBJECTS[subjectName] =  subjectID


def get_answer_by_id(id, lesson, subject, class_):
    HEADERS["Referer"] = "https://resh.edu.ru/subject/lesson/{0}/train/".format(lesson)
    out = []
    with requests.Session() as session:
        r = session.post(r"https://resh.edu.ru/", headers=HEADERS)
        COOKIES["PHPSESSID"] = r.cookies["PHPSESSID"]
        answerRequest = session.post("https://resh.edu.ru/tests/{0}/get-answers".format(id), headers=HEADERS, cookies=COOKIES)
        for msg in answerRequest.iter_lines():
            out.append(json.loads(msg))
        with open("{0}-{1} класс-{2} урок-{3} задание.json".format(subject, class_, lesson, id), "w", encoding="utf-8") as f:
            json.dump(out, f, indent=4, ensure_ascii=False)
        return out


def parse_answers(lessonID, lesson_, subject_, class_):
    testIDs = []
    req = requests.get("https://resh.edu.ru/subject/lesson/{0}/train/".format(lessonID))
    soup = bs(req.text, "html.parser")
    
    tests = soup.find_all("li", {"class": "test__task-num"})
    for test in tests:
        testIDs.append(test["data-test-id"])
    for id in testIDs:
        get_answer_by_id(id, lesson_, subject_, class_)


def get_lesson_id(sbj, cls, lsn):
    output = []
    page = 1
    subjectURL = "{}/subject/{}/{}".format(mainURL, SUBJECTS[sbj], cls)

    while True:
        html = requests.post(subjectURL + "/ajax?page={}".format(page), headers=HEADERS).json()["html"]
        lessonBlocks = bs(html, "html.parser").find_all("a", {"class": "lesson-block"})
        for link in lessonBlocks:
            output.append(str(link.get("href")).strip("/subject/lesson"))
        page += 1

        if page > 4:
            break
    
    return output[lsn - 1]
    
start_time = time.time()
setup()
print(time.time() - start_time)
subject = input("Введите название предмета: ")
class_ = int(input("Введите класс: "))
lesson = int(input("Введите номер урока: "))
id = get_lesson_id(subject, class_, lesson)
parse_answers(id, lesson, subject, class_)
























































































































