from flask import Flask, render_template
app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/index")
def index():
    return render_template("index.html", message="test")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
