from flask import Flask, render_template, request
from models.model.logistic import Logistic
import json
import subprocess


app = Flask(__name__)
m = Logistic()
m.load_model(fname="sentplot.npy")

with open("models/dataset/concat.csv") as f:
    lines = [line.replace("\n", "") for line in f.readlines()]

train_data = {t[2:]: t[:2] for t in lines[:-100]}
train_sents = [k for k in train_data.keys()]
train_signs = [int(v) for v in train_data.values()]
logistic = Logistic(train_sents, train_signs)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/train")
def train():
    logistic.train()
    return render_template("train.html")


@app.route("/form")
def form_before_POST():
    make_sample_vecs_to_json()
    return render_template("form.html")


@app.route("/form", methods=["POST"])
def form():
    if request.method == "POST":
        sentence = request.form["sentence"]
    result = m.predict(sentence)
    sign, per, vec = result
    vec = list(vec)
    w = list(m.w)
    make_sample_vecs_to_json()
    return render_template("form.html", w=w, text=sentence,
                           textvec=[float(vec[0]), float(vec[1])])


def dict_to_json(dic: dict, name: str):
    with open("static/json/" + name, "w") as f:
        json.dump(dic, f)


def make_sample_vecs_to_json():
    with open("models/dataset/concat.csv") as f:
        lines = [line.replace("\n", "")[2:] for line in f.readlines()]
    test = lines[-50:]
    dic = {-1: {}, 1: {}}
    for t in test:
        p = m.predict(t)
        dic[p[0]][t] = list(p[2])
    j = {"sentences": [], "vecs": {"x": [], "y": []}, "sign": []}
    for k, v in dic.items():
        for sentence, vector in v.items():
            j["sentences"].append(sentence)
            j["vecs"]["x"].append(float(vector[0]))
            j["vecs"]["y"].append(float(vector[1]))
            j["sign"].append(k)
    dict_to_json(j, "test.json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
