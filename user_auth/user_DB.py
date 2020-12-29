from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SQL access layer initialization
DATABASE_FILE = "users.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), connect_args={'check_same_thread': False}, echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    name = Column(String)
    role = Column(String)
    videos_reg = Column(Integer, default = 0)
    views = Column(Integer, default = 0)
    questions = Column(Integer, default = 0)
    answers = Column(Integer, default = 0)
    def __repr__(self):
        return "<Users (id=%d, user=%s, name = %s, role=%s, videos_reg =%d, views =%d, questions =%d, answers =%d>" % (
                        self.id, self.user, self.name, self.role, self.videos_reg, self.views, self.questions, self.answers)
    def to_dictionary(self):
        return {"id": self.id, "user": self.user, "name" : self.name, "role" : self.role, "videos_reg": self.videos_reg, "views": self.views, "questions": self.questions, "answers": self.answers}



Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listUsers():
    return session.query(Users).all()
    session.close()


def getUser(user):
     v =  session.query(Users).filter(Users.user==user).all()
     session.close()
     return v

def listUsersDICT():
    ret_list = []
    logs = listUsers()
    for l in logs:
        ls = l.to_dictionary()
        ret_list.append(ls)
    return ret_list

def listUDICT(user):
    ret_list = []
    logs = getUser(user)
    for l in logs:
        ls = l.to_dictionary()
        ret_list.append(ls)
    return ret_list

def newUser(user, name, role):
    uid = Users(user = user, name = name, role = role)
    try:
        session.add(uid)
        session.commit()
        v = uid.id
        session.close()
        return v
    except:
        return None

def newVideoView(user):
    b = session.query(Users).filter(Users.user==user).first()
    b.views+=1
    n = b.views
    session.commit()
    session.close()
    return n


def newQuestion(user):
    b = session.query(Users).filter(Users.user==user).first()
    b.questions+=1
    n = b.questions
    session.commit()
    session.close()
    return n

def newAnswer(user):
    b = session.query(Users).filter(Users.user==user).first()
    b.answers+=1
    n = b.answers
    session.commit()
    session.close()
    return n

def newVideoReg(user):
    b = session.query(Users).filter(Users.user==user).first()
    b.videos_reg+=1
    n = b.videos_reg
    session.commit()
    session.close()
    return n


if __name__ == "__main__":
    pass