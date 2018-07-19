from flask import Flask, render_template, request
from models.model.logistic import Logistic
import json


app = Flask(__name__)
m = Logistic()
m.load_model(fname="sentplot.npy")


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/form")
def form():
    return render_template("form.html")


@app.route("/sentplot", methods=["POST"])
def sentplot():
    if request.method == "POST":
        sentence = request.form["sentence"]
    result = m.predict(sentence)
    sign, per, vec = result
    vec = list(vec)
    w = list(m.w)
    make_sample_vecs_to_json()
    return render_template("sentplot.html",
                           w=w, sign=sign, per=per, vec=vec, dic="dic")


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
    with open("static/test.json", "w") as f:
        json.dump(j, f)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
