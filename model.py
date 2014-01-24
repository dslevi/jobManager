import config
import bcrypt
from datetime import datetime
import time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
from flask.ext.login import UserMixin

engine = create_engine(config.DB_URI, echo=False)
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property()
 
class User(Base, UserMixin):
    __tablename__ = "users" 
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    email = Column(String(64), nullable=False)
    password = Column(String(64), nullable=False)
    salt = Column(String(64), nullable=False)

    deadline = Column(DateTime, default=datetime.now)
    numApplications = Column(Integer, default=0)
    points = Column(Integer, default=0)
    employed = Column(Boolean, default=False)

    # industry = Columnn(String(64), nullable=False)
    # position = Column(String(64), nullable=False)
    # figure out how to get coordinates
    # location = Column(String(64), nullable=False)
    # linkedin/fb api connects

    badges = relationship("Badge", uselist=True)
    # resumes = relationship("Resume", uselist=True)
    tasks = relationship("UserTask", uselist=True)
    companies = relationship("Company", uselist=True)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

class TaskTemplate(Base):
    __tablename__ = "taskTemplates"
    id = Column(Integer, primary_key=True)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    points = Column(Integer, default=0)
    category = Column(Integer, default=0)
    imgPath = Column(String(64), nullable=False)
    difficulty = Column(Integer, default=0)

    taskInstances = relationship("UserTask", uselist=True)

class BadgeTemplate(Base):
    __tablename__ = "badgeTemplates"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    imgPath = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)

    badgeInstances = relationship("Badge", uselist=True)

#ONE TO MANY

# class Resume(Base):
#     __tablename__ = "resumes"
#     id = Column(Integer, primary_key=True)
#     filePath = Column(String(64), nullable=False)
#     uploadDate = Column(DateTime, nullable=False, default=datetime.now)
#     userId = relationship("User")

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    position = Column(Text, nullable=False)
    phone = Column(Integer, nullable=True)
    address = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    status = Column(Integer, default=0)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    contacts = relationship("Contact", uselist=True)
    interviews = relationship("Interview", uselist=True)
    tasks = relationship("UserTask", uselist=True)

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    contactInfo = Column(Text, nullable=False)
    notes = Column(Text, nullable=True)
    contacted = Column(Boolean, default=False)

    companyId = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company")

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True)
    deadline = Column(DateTime, default=datetime.now)
    notes = Column(Text, nullable=True)
    feedback = Column(Text, nullable=True)
    completed = Column(Boolean, default=False)

    companyId = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company")

#MANY TO MANY

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    badgeId = Column(Integer, ForeignKey("badgeTemplates.id"))
    badge = relationship("BadgeTemplate")

class UserTask(Base):
    __tablename__ = "userTasks"
    id = Column(Integer, primary_key=True)
    dateAssigned = Column(DateTime, default=datetime.now)
    dateCompleted = Column(DateTime, default=datetime.now)
    completed = Column(Boolean, default=False)

    userId = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")
    taskId = Column(Integer, ForeignKey("taskTemplates.id"))
    task = relationship("TaskTemplate")
    companyId = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company")


# Model methods

def getCurrentTasks(userId):
    user = User.query.get(userId)
    tasklist = user.tasks
    tasks = []
    for task in tasklist:
        if not task.completed:
            t = TaskTemplate.query.get(task.taskId)
            title = t.summary
            tasks.append(title)
    return tasks

def createUser(email, password):
    user = User(email=email)
    user.set_password(password)
    session.add(user)
    session.commit()
    for i in range(1, 5):
        t = UserTask(userId=user.id, taskId=i, companyId=0)
        session.add(t)
    session.commit()

# Table creation/ seed data

def create_tables():
    Base.metadata.create_all(engine)
    u = User(name="Danielle", email="dslevi12@gmail.com")
    u.set_password("python")
    session.add(u)
    u2 = User(name="Hidi", email="nahid@gmail.com")
    u2.set_password("hackbright")
    session.add(u2)
    t = TaskTemplate(summary="This is a short summary", description="This is a long description with many things", imgPath="/task1")
    session.add(t)
    session.commit()
    c = Company(name="Skybox Imaging", position="Software Engingeer", userId=u.id)
    session.add(c)
    session.commit()
    task = UserTask(userId=u.id, taskId=t.id, companyId=c.id)
    session.add(task)
    session.commit()
    print "Tables completed"

def create_taskTemplates():
    print "Task templates created"

if __name__ == "__main__":
    create_tables()
    create_taskTemplates()

