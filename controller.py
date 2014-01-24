from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
from model import User, TaskTemplate, BadgeTemplate, Company, Contact, Interview, Badge, UserTask
import config, model

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    if session.get('userId'):
        userId = session['userId']
        active, passive = model.getCurrentTasks(userId)
        return render_template("home.html", active=active, passive=passive)
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/validate", methods=["POST"])
def validate():
    email = request.form.get('email')
    password = request.form.get('password')
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
    email = request.form.get('email')
    password = request.form.get('password')
    verify = request.form.get('verify')
    if User.query.filter_by(email=email).all():
        flash("Email already exists")
        return redirect(url_for("register"))
    if password != verify:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    model.createUser(email, password)
    return redirect(url_for("login"))

@app.route("/signout")
def signout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/help")
def help():
    return render_template("help.html")

# In Progress

@app.route("/forgotpassword")
def recover():
    return render_template("recover.html")

@app.route("/companies")
def companies():
    #query for user and find companies
    return render_template("companies.html")

@app.route("/schedule")
def schedule():
    #query for user and find the schedule
    return render_template("schedule.html")

@app.route("/task/<taskId>")
def displayDetails(taskId):
    task = UserTask.query.get(taskId)
    #check that user task belongs to this user!
    if task.userId != session['userId']:
        return render_template("incorrect.html")
    return render_template("taskDetails.html", task=task)

#COMPANY HANDLERS

@app.route("/task/createcompany/<tId>")
def createCompany():
    #get values from form fields
    #create company
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifycompany/<tId>")
def modifyCompany():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/companyrejection/<tId>")
def deleteCompany():
    #FILL IN LOGIC (change status)
    return redirect(url_for("completedTask", tId=tId))

#CONTACT HANDLERS

@app.route("/task/createcontact/<tId>")
def createContact():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifycontact/<tId>")
def modifyContact():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

#INTERVIEW HANDLERS

@app.route("/task/createinterview/<tId>")
def createInterview():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifyinterview/<tId>")
def modifyInterview():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

#TASK HANDLERS

@app.route("/task/completed/<tId>")
def completedTask(tId):
    model.completeTask(tId, session['userId'])
    #some sort of alert or congrats message pop-up
    return redirect(url_for("index"))

@app.route("/task/makepassive/<tId>")
def makePassive(tId):
    #Query for task and make it passive
    #This could be AJAX
    return redirect(url_for("index"))

#BADGE HANDLERS

@app.route("/badges/createbadge/<bId>")
    #create instance of badge
    #This could be AJAX
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
