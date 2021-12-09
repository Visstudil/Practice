import requests

COOKIES = {"PHPSESSID": ""}
HEADERS = {"User-Agent":         "Chrome/94.0.4606.71",
            "Accept" :           "*/*",
            "Accept-Language":   "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "X-Requested-With":  "XMLHttpRequest"}
PAYLOAD = {"answers": '{"154781":{"RESPONSE1_1":"2"},"154784":{"RESPONSE1":["A","B","C"]},"154787":{"RESPONSE1":["B F","C G","D H"]},"154790":{"RESPONSE1_1":""},"154791":{"RESPONSE1_1":""},"154792":{"RESPONSE1_1":""},"154794":{"RESPONSE1":["A"]},"154796":{"RESPONSE1_1":"\\n        \\n        \\n      "}}'}

with requests.Session() as s:
    r = s.post("https://resh.edu.ru/", headers=HEADERS)
    COOKIES["PHPSESSID"] = s.cookies["PHPSESSID"]
    print("PHPSESSID=%s" % COOKIES["PHPSESSID"])
    print(s.post("https://resh.edu.ru/subject/lesson/1548/train/result/", headers=HEADERS, cookies=COOKIES, data=PAYLOAD).text)