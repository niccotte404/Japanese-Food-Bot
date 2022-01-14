import json

with open("stopwords.txt", encoding="utf-8") as words:
    for w in words:
        w = w.lower()
        lst = w.split(" ")

with open("stopwords.json", "w", encoding="utf-8") as f:
    json.dump(lst, f)