from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def login():
    return render_template("instructors/index.html")


if __name__ == '__main__':
    app.run(debug=True)
    