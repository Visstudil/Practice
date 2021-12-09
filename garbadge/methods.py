import os
from random import randint
import pymorphy2

morph = pymorphy2.MorphAnalyzer(lang="ru")

def readlist(path):
    out = []
    with open(path, "r") as f:
        for line in f.readlines:
            out.append(line)
    return out

def createifnotexist(path):
    if not os.path.exists(path):
        if os.path.isdir(path):
            os.mkdir(path)
        else:
            open(path, "x").close()

def incline(path, attr):  # Inclines words in the text file to {attr} and writes them on this text file
    out = []
    with open(path, "r") as fr:
        for line in fr.readlines():
            w = morph.parse(line)[0]
            out.append(w.inflect(attr).word)
    with open(path, "a") as fw:
            fw.writelines(out)


def appendlines(path, lines):
    l = lines
    with open(path, "r") as f:
        for line in f.readlines():
            if line in lines:
                l.remove(line)
    with open(path, "a") as f:
        f.writelines(l)

def formatstr(a, b, formatString="\n{0} из {1}", isRandom=True):
    out = []
    if (len(a), len(b)) != (0, 0):
        if isRandom:
            for line in a:
                out.append(formatString.format(line, b[randint(0, len(b)-1)]))
        else:
            for linea in a:
                for lineb in b:
                    out.append(formatString.format(linea, lineb))
    return out