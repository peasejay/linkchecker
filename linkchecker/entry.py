from linkchecker import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import LONGTEXT

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    feed = relationship("Feed", back_populates="entries")
    vendor_code = Column(String(255), nullable=False)
    title = Column(String(255))
    author = Column(String(255))
    summary = Column(LONGTEXT())
    content = Column(LONGTEXT())
    link = Column(String(255))
    published = Column(DateTime(timezone=True))
    updated = Column(DateTime(timezone=True))
    pinged = Column(DateTime(timezone=True))


    def __repr__(self):
        return "<Entry(id='%d', title='%s', author='%s')>" % (int(self.id), self.title, self.author)