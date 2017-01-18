from linkchecker import Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship

class Site(Base):
    __tablename__ = 'sites'

    id = Column(Integer, primary_key=True)
    code = Column(String(50), nullable=False)
    title = Column(String(255))
    link = Column(String(255))
    tags = Column(String(255))
    updated = Column(DateTime(timezone=True))
    feeds = relationship("Feed", back_populates="site")

    @classmethod
    def get_by_code(self, code):
        return session.query(self).filter(self.code == code).first()

    def __repr__(self):
        return "<Site(id='%d', code='%s', title='%s')>" % (int(self.id), self.code, self.title)
