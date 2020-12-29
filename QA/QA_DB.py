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

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), connect_args={'check_same_thread': False}, echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class QA(Base):
    __tablename__ = 'QA'
    id = Column(Integer, primary_key=True)
    video_id = Column(String)
    user = Column(String)
    name = Column(String)
    time = Column(String)
    question = Column(String)
    def __repr__(self):
        return "<QA (id=%d, video_id =%s, user =%s, name =%s, time=%s, question=%s>" % (
                        self.id, self.video_id, self.user, self.name, self.time, self.question)
    def to_dictionary(self):
        return {"QA_id": self.id, "video_id": self.video_id, "user": self.user,"name": self.name, "time": self.time, "question": self.question}

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


def listQA(id):
    return session.query(QA).filter(QA.video_id==id).all()
    session.close()

def listQADICT(id):
    ret_list = []
    lqa = listQA(id)
    for q in lqa:
        qa = q.to_dictionary()
        ret_list.append(qa)
    print(ret_list)
    return ret_list

def listQuestion(id, q_id):
    return session.query(QA).filter(QA.video_id==id, QA.id==q_id)
    session.close()

def listQuestionDICT(id, q_id):
    ret_list = []
    lqa = listQuestion(id, q_id)
    for q in lqa:
        qa = q.to_dictionary()
        ret_list.append(qa)
    print(ret_list)
    return ret_list

def getQuestion(id):
     q =  session.query(QA).filter(QA.id==id).scalar()
     session.close()
     return q

def getQDICT(id):
    return getQuestion(id).to_dictionary()

def newQuestion(v_id, user, name, time, question):
    uid = QA(video_id = v_id, user = user, name = name, time = time, question = question)
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
    v =  session.query(Answer).filter(Answer.question==question_id ).all()
    session.close()
    return v


def listAnswersDICT(question_id):
    ret_list = []
    lv = listAnswers(question_id)
    for v in lv:
        vd = v.to_dictionary()
        ret_list.append(vd)
    return ret_list


if __name__ == "__main__":
    pass