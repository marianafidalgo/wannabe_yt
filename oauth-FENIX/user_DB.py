from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "users.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    number = Column(String)
    name = Column(String)
    role = Column(String)
    def __repr__(self):
        return "<User (id=%d, number=%s, name=%s, role=%s>" % (
                                self.id, self.number, self.name, self.role)
    def to_dictionary(self):
        return {"user_id": self.id, "number": self.number, "name": self.name, "role": self.role}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listUsers():
    return session.query(Users).all()
    session.close()

def listVideosDICT():
    ret_list = []
    lv = listVideos()
    for v in lv:
        vd = v.to_dictionary()
        del(vd["url"])
        del(vd["views"])
        ret_list.append(vd)
    return ret_list

def getUser(number):
     v =  session.query(Users).filter(Users.number==number).scalar()
     session.close()
     return v

def getUserDICT(id):
    return getUser(id).to_dictionary()

def newUser(number, name, role):
    uid = Users(number = number, name = name, role = role)
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