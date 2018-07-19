from flask import Flask, render_template, request
from models.model.logistic import Logistic
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
    return render_template("sentplot.html", w=w, sign=sign, per=per, vec=vec)


def return_sample_vecs():
    with open("models/dataset/concat.csv") as f:
        lines = [line.replace("\n", "")[2:] for line in f.readlines()]
    test = lines[-50:]
    dic = {-1: {}, 1: {}}
    for t in test:
        p = m.predict(t)
        dic[p[0]][t] = p[2]
    return dic


if __name__ == "__main__":
    app.run(host="1.0.0.0", debug=True)
