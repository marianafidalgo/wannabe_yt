from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SQL access layer initialization
DATABASE_FILE = "qa.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class QA(Base):
    __tablename__ = 'QA'
    id = Column(Integer, primary_key=True)
    time = Column(String)
    question = Column(String)
    def __repr__(self):
        return "<QA (id=%d, time=%s, question=%s>" % (
                                self.id, self.time, self.question)
    def to_dictionary(self):
        return {"QA_id": self.id, "time": self.time, "question": self.question}

class Answer(Base):
    __tablename__ = 'Answer'
    id = Column(Integer, primary_key=True)
    #question_id = Column(Integer, ForeignKey('QA.id'))
    user = Column(String)
    name = Column(String)
    answer = Column(String)
    question = Column(String)
    #question = relationship("QA", backref="Answer")
    def __repr__(self):
        return "<Answer ( id=%d, user=%s, name=%s, answer=%s, question=%s>" % (
                            self.id, self.user, self.name, self.answer, self.question)
    def to_dictionary(self):
        return {"Answer": self.id, "user": self.user, "name": self.name, "answer": self.answer, "question": self.question}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listQA():
    return session.query(QA).all()
    session.close()

def listQADICT():
    ret_list = []
    lv = listQA()
    for v in lv:
        vd = v.to_dictionary()
        # del(vd["url"])
        # del(vd["views"])
        ret_list.append(vd)
    return ret_list

def getQuestion(id):
     v =  session.query(QA).filter(QA.id==id).scalar()
     session.close()
     return v

def getQDICT(id):
    return getQuestion(id).to_dictionary()

def newQuestion(time, question):
    uid = QA(time = time, question = question)
    try:
        session.add(uid)
        session.commit()
        v = uid.id
        session.close()
        return v
    except:
        return None

def newAnswer(user, name, answer, question):
    uid = Answer(user = user, name = name, answer = answer, question = question)
    try:
        session.add(uid)
        session.commit()
        v = uid.id
        session.close()
        return v
    except:
        return None

def listAnswers(question_id):
    v =  session.query(Answer).filter(Answer.question==question_id).all()
    session.close()
    return v


def listAnswersDICT(question_id):
    ret_list = []
    lv = listAnswers(question_id)
    for v in lv:
        vd = v.to_dictionary()
        #del(vd["question"])
        # del(vd["views"])
        ret_list.append(vd)
    return ret_list


if __name__ == "__main__":
    pass