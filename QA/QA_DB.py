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


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listQA():
    return session.query(QA).all()
    session.close()

# def listVideosDICT():
#     ret_list = []
#     lv = listVideos()
#     for v in lv:
#         vd = v.to_dictionary()
#         del(vd["url"])
#         del(vd["views"])
#         ret_list.append(vd)
#     return ret_list

def getQuestion(id):
     v =  session.query(QA).filter(QA.id==id).scalar()
     session.close()
     return v

def getQuestionDICT(id):
    return getUser(id).to_dictionary()

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



if __name__ == "__main__":
    pass