from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
from model import User, TaskTemplate, BadgeTemplate, Company, Contact, Interview, Badge, UserTask, session
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    user = User.query.get(1)
    print "name ", user.name
    print "companies ", user.companies
    tasks = [1, 2, 3]
    return render_template("home.html", tasks=tasks)
    # if session.get('userId'):
    #     tasks = User.query.get(session['userId']).one().tasks
    #     return render_template("home.html", tasks=tasks)
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/validate", methods=["POST"])
def validate():
    email = request.forms.get('email')
    password = request.forms.get('password')
    user = User.query.filter_by(email=email).one()
    if user.authenticate(password):
        session['userId'] = user.id
        return redirect(url_for('index'))
    else:
        flash("Invalid username or password")
        return redirect(url_for('login'))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/registerUser", methods=["POST"])
def registerUser():
    email = request.forms.get('email')
    password = request.forms.get('password')
    verify = request.forms.get('verify')
    if user.query.filter_by(email=email).all():
        flash("Email already exists")
        return redirect(url_for("register"))
    if password != verify:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    user = User(email=email)
    user.set_password(password)
    session.add(user)
    session.commit()
    return redirect(url_for("login"))

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/companies")
def companies():
    #query for user and find companies
    return render_template("companies.html")

@app.route("/schedule")
def schedule():
    #query for user and find the schedule
    return render_template("schedule.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/task/<taskId>")
def displayDetails(taskId):
    # task = UserTake.query.get(taskId)
    task = "<form><input type='text'></input></form>"
    return render_template("taskDetails.html", task=task)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
