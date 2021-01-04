from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SQL access layer initialization
DATABASE_FILE = "logs.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), connect_args={'check_same_thread': False}, echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Events(Base):
    __tablename__ = 'Events'
    id = Column(Integer, primary_key=True)
    url = Column(String)
    timestamp = Column(String)
    def __repr__(self):
        return "<Events (id=%d, url =%s, timestamp =%s>" % (
                        self.id, self.url, self.timestamp)
    def to_dictionary(self):
        return {"id": self.id, "url": self.url,"timestamp": self.timestamp}

class DataCreation(Base):
    __tablename__ = 'DataCreation'
    id = Column(Integer, primary_key=True)
    #question_id = Column(Integer, ForeignKey('QA.id'))
    data_type = Column(String)
    content = Column(String)
    timestamp = Column(String)
    user = Column(String)
    #question = relationship("QA", backref="Answer")
    def __repr__(self):
        return "<DataCreation ( id=%d, data_type=%s, content=%s, timestamp=%s, user=%s>" % (
                            self.id, self.data_type, self.content, self.timestamp, self.user)
    def to_dictionary(self):
        return {"DataCreation": self.id, "data_type": self.data_type, "content": self.content, "timestamp": self.timestamp, "user": self.user}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listDC():
    return session.query(DataCreation).all()
    session.close()

def listDCDICT():
    ret_list = []
    logs = listDC()
    for l in logs:
        ls = l.to_dictionary()
        ret_list.append(ls)
    return ret_list

def newDC(data_type, content, timestamp, user):
    uid = DataCreation(data_type = data_type, content = content, timestamp = timestamp, user = user)
    try:
        session.add(uid)
        session.commit()
        session.refresh(uid)
        v = uid.id
        session.close()
        return v
    except:
        return None

def listEvent():
    return session.query(Events).all()
    session.close()

def listEventsDICT():
    ret_list = []
    logs = listEvent()
    for l in logs:
        ls = l.to_dictionary()
        ret_list.append(ls)
    return ret_list

def newEvent(timestamp, url):
    uid = Events(timestamp = timestamp, url = url)
    try:
        session.add(uid)
        session.commit()
        session.refresh(uid)
        v = uid.id
        session.close()
        return v
    except:
        return None

if __name__ == "__main__":
    pass