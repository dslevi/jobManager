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
    phone = Column(Integer, nullable=True)

    deadline = Column(DateTime, default=datetime.now)
    numApplications = Column(Integer, default=0)
    points = Column(Integer, default=0)
    employed = Column(Boolean, default=False)
    company = Column(String(64), nullable=True)
    industry = Columnn(String(64), nullable=False)
    position = Column(String(64), nullable=False)
    
    #find out how to do locations
    location = Column(String(64), nullable=False)

    #linkedin
    #fb

    badges = relationship("Badge", uselist=True)
    resumes = relationship("Resume", uselist=True)
    completedTasks = relationship("Task", uselist=True)
    waitingTasks = relationship("Task", uselist=True)

    def set_password(self, password):
        self.salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        self.password = bcrypt.hashpw(password, self.salt)

    def authenticate(self, password):
        password = password.encode("utf-8")
        return bcrypt.hashpw(password, self.salt.encode("utf-8")) == self.password

#ONE (USER) TO MANY

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True)
    filePath = Column(String(64), nullable=False)
    uploadDate = Column(DateTime, nullable=False, default=datetime.now)
    userId = relationship("User")

#MANY (USERS) TO MANY --- FIND OUT HOW TO DO BACKREFS

class Badge(Base):
    __tablename__ = "badges"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=True)
    imgPath = Column(String(64), nullable=False)
    description = Column(Text, nullable=False)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    summary = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    points = Column(Integer, default=0)
    imgPath = Column(String(64), nullable=False)

def create_tables():
    Base.metadata.create_all(engine)
    print "Tables completed"


if __name__ == "__main__":
    create_tables()

