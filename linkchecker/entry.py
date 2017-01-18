from linkchecker import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    feed = relationship("Feed", back_populates="entries")
    vendor_code = Column(String(255), nullable=False)
    title = Column(String(255))
    author = Column(String(255))
    summary = Column(Text())
    content = Column(Text())
    link = Column(String(255))
    pinged = Column(DateTime(timezone=True), onupdate=func.now())


    def __repr__(self):
        return "<Entry(id='%d', title='%s', author='%s')>" % (int(self.id), self.title, self.author)