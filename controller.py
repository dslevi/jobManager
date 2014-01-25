from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
from model import User, TaskTemplate, BadgeTemplate, Company, Contact, Interview, Badge, UserTask
import config, model

app = Flask(__name__)
app.config.from_object(config)

@app.route("/")
def index():
    if session.get('userId'):
        active, passive = model.getCurrentTasks(session['userId'])
        user = User.query.get(session['userId'])
        return render_template("home.html", active=active, passive=passive, user=user)
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
    #creates user row and also starter tasks
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
    #query for user and email pw recovery link
    return render_template("recover.html")

@app.route("/companies")
def companies():
    if not session.get('userId'):
        return redirect(url_for("login"))
    active, passive = model.getCurrentTasks(session['userId'])
    activeCompanies, rejectedCompanies = model.displayCompanies(session['userId'])
    user = User.query.get(session['userId'])
    return render_template("companies.html", active=active, passive=passive, activeCompanies=activeCompanies, rejectedCompanies=rejectedCompanies, user=user)

@app.route("/schedule")
def schedule():
    if not session.get('userId'):
        return redirect(url_for("login"))
    active, passive = model.getCurrentTasks(session['userId'])
    #query for user and find the schedule
        #contains interviews, events, deadlines
    user = User.query.get(session['userId'])
    return render_template("schedule.html", active=active, passive=passive, user=user)

@app.route("/task/<tId>")
def displayDetails(tId):
    if not session.get('userId'):
        return redirect(url_for("login"))
    #check if task exists in db
    if not authorized(tId):
        return render_template("unauthorized.html")
    #check if task is not completed
    t = UserTask.query.get(tId)
    if t.completed:
        return render_template("oldTask.html")
    task = TaskTemplate.query.get(t.taskId)
    active, passive = model.getCurrentTasks(session['userId'])
    user = User.query.get(session['userId'])
    return render_template("taskDetails.html", task=task, active=active, passive=passive, user=user)

######################## CRUD HANDLERS ########################

#COMPANY HANDLERS

@app.route("/task/createcompany/<tId>")
def createCompany():
    name = request.form.get('name')
    position = request.form.get('position')
    phone = request.form.get('phone')
    address = request.form.get('address')
    c = Company(name=name, position=position, phone=phone,
        address=address, userId=session['userId'])
    model.session.add(c)
    model.session.commit()
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifycompany/<tId>")
def modifyCompany():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/companyrejection/<tId>")
def deleteCompany():
    task = UserTask.query.get(tId)
    company = Company.query.get(task.companyId)
    company.status = 0
    model.session.commit()
    return redirect(url_for("completedTask", tId=tId))

#CONTACT HANDLERS

@app.route("/task/createcontact/<tId>")
def createContact():
    name = request.form.get('name')
    contactInfo = request.form.get('contactInfo')
    task = UserTask.query.get(tId)
    companyId = task.companyId
    contact = Contact(name=name, contactInfo=contactInfo, companyId=companyId)
    model.session.add(contact)
    model.session.commit()
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifycontact/<tId>")
def modifyContact():
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

#INTERVIEW HANDLERS

@app.route("/task/createinterview/<tId>")
def createInterview():
    deadline = request.form.get('deadline')
    task = UserTask.query.get(tId)
    companyId = task.companyId
    interview = Interview(deadline=deadline, companyId=companyId)
    model.session.add(interview)
    model.session.commit()
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifyinterview/<tId>")
def modifyInterview():
    #FILL IN LOGIC
    #Ex. add note, make changes to entered data?
    return redirect(url_for("completedTask", tId=tId))

#NOTE HANDLERS

@app.route("/task/createCompanyNote/<tId>")
def createNote(tId):
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/modifyCompanyNote/<tId>")
def modifyNote(tId):
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

@app.route("/task/deleteCompanyNote/<tId>")
def deleteNote(tId):
    #FILL IN LOGIC
    return redirect(url_for("completedTask", tId=tId))

#TASK HANDLERS

#completeTask completes current task and creates new tasks
@app.route("/task/completed/<tId>")
def completedTask(tId):
    model.completeTask(tId, session['userId'])
    #some sort of alert or congrats message pop-up
    return redirect(url_for("index"))

#!!!!Make this AJAX!!!!
@app.route("/task/makepassive/<tId>")
def makePassive(tId):
    if not authorized(tId):
        return redirect(url_for("unauthorized"))
    task = UserTask.query.get(tId)
    task.passive = True
    model.session.commit()
    return redirect(url_for("index"))

#BADGE HANDLERS

#!!!!Make this AJAX!!!!
@app.route("/badges/createbadge/<bId>")
def createBadge():
    badge = Badge(userId=session['userId'], badgeId=bId)
    model.session.add()
    model.session.commit()
    return redirect(url_for("index"))

### HELPER FUNCTION ###

@app.route("/unauthorized")
def unauthorized():
    #flash warning for why
    return render_template("unauthorized.html")

#checks if task exists in db and user is authorized to access it
def authorized(tId):
    if not UserTask.query.get(tId):
        return False
    t = UserTask.query.get(tId)
    return t.userId == session['userId']

if __name__ == "__main__":
    app.run(debug=True, port=5001)
