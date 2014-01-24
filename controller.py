from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
import model
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<taskId>")
def displayDetails(taskId):
    # task = UserTake.query.get(taskId)
    task = "<form><input type='text'></input></form>"
    return render_template("taskDetails.html", task=task)

@app.route("/hello")
def test():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
