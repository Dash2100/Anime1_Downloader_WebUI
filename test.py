import json


def writejson(data):
    with open('data/cache.json', 'w', encoding="UTF-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))


with open('data/cache.json', 'r', encoding="UTF-8") as f:
    json_file = json.load(f)

all_title = []
for d in json_file['waiting']:
    all_title.append(list(d.keys())[0])
print(all_title.index("名偵探柯南 犯人·犯澤先生"))
json_file['waiting'].pop(all_title.index("名偵探柯南 犯人·犯澤先生"))
print(json_file)