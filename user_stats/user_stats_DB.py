from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SQL access layer initialization
DATABASE_FILE = "stats.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), connect_args={'check_same_thread': False}, echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Stats(Base):
    __tablename__ = 'Stats'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    videos_reg = Column(Integer, default = 0)
    views = Column(Integer, default = 0)
    questions = Column(Integer, default = 0)
    answers = Column(Integer, default = 0)
    def __repr__(self):
        return "<Stats (id=%d, user=%s, videos_reg =%d, views =%d, questions =%d, answers =%d>" % (
                        self.id, self.user, self.videos_reg, self.views, self.questions, self.answers)
    def to_dictionary(self):
        return {"id": self.id, "user": self.user, "videos_reg": self.videos_reg, "views": self.views, "questions": self.questions, "answers": self.answers}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listStats():
    return session.query(Stats).all()
    session.close()

def listStatsDICT():
    ret_list = []
    logs = listStats()
    for l in logs:
        ls = l.to_dictionary()
        ret_list.append(ls)
    print(ret_list)
    return ret_list

def newUser(user):
    print(user)
    if(session.query(Stats).filter(user==user).scalar() is None):
        uid = Stats(user = user)
        try:
            session.add(uid)
            session.commit()
            v = uid.id
            session.close()
            return v
        except:
            return None

def newVideoView(user):
    b = session.query(Stats).filter(Stats.user==user).first()
    b.views+=1
    n = b.views
    session.commit()
    session.close()
    return n


def newQuestion(user):
    b = session.query(Stats).filter(Stats.user==user).first()
    b.questions+=1
    n = b.questions
    session.commit()
    session.close()
    return n

def newAnswer(user):
    b = session.query(Stats).filter(Stats.user==user).first()
    b.answers+=1
    n = b.answers
    session.commit()
    session.close()
    return n

def newVideoReg(user):
    b = session.query(Stats).filter(Stats.user==user).first()
    b.videos_reg+=1
    n = b.videos_reg
    print(n)
    session.commit()
    session.close()
    return n

if __name__ == "__main__":
    pass