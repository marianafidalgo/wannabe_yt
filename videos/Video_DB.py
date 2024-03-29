from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, scoped_session

import datetime
from sqlalchemy.orm import sessionmaker
from os import path


#SLQ access layer initialization
DATABASE_FILE = "ytVideos.sqlite"
db_exists = False
if path.exists(DATABASE_FILE):
    db_exists = True
    print("\t database already exists")

engine = create_engine('sqlite:///%s'%(DATABASE_FILE), connect_args={'check_same_thread': False}, echo=False) #echo = True shows all SQL calls

Base = declarative_base()

#Declaration of data
class YTVideo(Base):
    __tablename__ = 'YTVideo'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    description = Column(String)
    url = Column(String)
    views = Column(Integer, default = 0)
    num_questions = Column(Integer, default = 0)
    def __repr__(self):
        return "<YouTubeVideo (id=%d, user=%s, description=%s, url=%s, views=%d, num_questions=%d>" % (
                                self.id, self.user, self.description, self.url,  self.views, self.num_questions )
    def to_dictionary(self):
        return {"video_id": self.id, "user":self.user, "description": self.description, "url": self.url, "views": self.views, "num_questions": self.num_questions}


Base.metadata.create_all(engine) #Create tables for the data models

Session = sessionmaker(bind=engine)
session = scoped_session(Session)
#session = Session()


def listVideos():
    return session.query(YTVideo).all()
    session.close()

def listVideosDICT():
    ret_list = []
    lv = listVideos()
    for v in lv:
        vd = v.to_dictionary()
        ret_list.append(vd)
    return ret_list

def getVideo(id):
     v =  session.query(YTVideo).filter(YTVideo.id==id).first()
     session.close()
     return v

def getVideoDICT(id):
    return getVideo(id).to_dictionary()

def newVideoView(id):
    b = session.query(YTVideo).filter(YTVideo.id==id).first()
    b.views+=1
    n = b.views
    session.commit()
    session.close()
    return n


def newQuestionSum(id):
    b = session.query(YTVideo).filter(YTVideo.id==id).first()
    b.num_questions+=1
    n = b.num_questions
    session.commit()
    session.close()
    return n

def newVideo(user, description , url):
    if(session.query(YTVideo).filter(YTVideo.url==url).scalar() is None):
        vid = YTVideo(user=user,description = description, url = url)
        try:
            session.add(vid)
            session.commit()
            v = vid.id
            session.close()
            return v
        except:
            return None



if __name__ == "__main__":
    pass