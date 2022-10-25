import logging
from django.shortcuts import render
from flask import Flask, render_template, request
from Downloader import Anime
import json
from os import listdir, remove
from os.path import isfile, isdir, join
import shutil

app = Flask(__name__)

# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)

def writejson(data):
    with open('data/cache.json', 'w', encoding="UTF-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))

@app.route("/")
def main():
    return render_template("index.html")


@app.route("/history", methods=['GET'])
def history():
    all_path = []
    mypath = "./Downloads"
    files = listdir(mypath)
    for f in files:
        fullpath = join(mypath, f)
        if isdir(fullpath):
            all_path.append(f)
    return render_template("history.html", **locals())


@app.route("/history/<string:name>", methods=['GET'])
def listvid(name):
    all_path = []
    mypath = f"./Downloads/{name}"
    try:
        files = listdir(mypath)
    except FileNotFoundError:
        return "Not Found"
    for f in files:
        fullpath = join(mypath, f)
        if isfile(fullpath):
            all_path.append(f)
    return render_template("listvid.html", **locals())


@app.route("/delani/<string:name>", methods=['GET'])
def delani(name):
    try:
        path = f"./Downloads/{name}"
        shutil.rmtree(path)
        return "ok"
    except:
        return "error"


@app.route("/stop", methods=['GET'])
def stop():
    with open('data/cache.json', 'r+', encoding="UTF-8") as f:
        data = json.load(f)
        if data['status'] == True:
            data['stop'] = True
            # data['status'] = False
            data['downloading_URL'] = ""
            data['downloading'] = {}
            f.seek(0)
            f.write(json.dumps(data, indent=4, ensure_ascii=False))
            f.truncate()
            return "OK"
        else:
            return "Not Downloading"


@app.route("/rmqueue/<string:name>", methods=['GET'])
def rmqueue(name):
    with open('data/cache.json', 'r', encoding="UTF-8") as f:
        json_file = json.load(f)

    all_title = []
    for d in json_file['waiting']:
        all_title.append(list(d.keys())[0])
    if name in all_title:
        json_file['waiting'].pop(all_title.index(name))
        writejson(json_file)
        return "OK"
    else:
        return "Not Found"
        


@app.route("/form", methods=['POST'])
def downloadPOST():
    url = request.form.get('url')
    return Anime(url)


@app.route("/getData", methods=['GET'])
def getData():
    try:
        with open('data/cache.json', 'r', encoding="UTF-8") as f:
            data = json.load(f)
        return data
    except:
        return {"status": "Error"}

print("http://127.0.0.1:5000")

if __name__ == "__main__":
    # 清除快取
    data = {
        "status": False,
        "downloading": {},
        "waiting": [],
        "downloading_URL": "",
        "stop": False
    }
    with open('data/cache.json', 'w') as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    # 開啟Web
    app.run(debug=True,host='0.0.0.0', port=5000)
    # app.run(debug=True)