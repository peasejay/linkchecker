from linkchecker import Base
from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from entry import Entry
import feedparser
import requests
import difflib

class Feed(Base):
    __tablename__ = 'feeds'

    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    site = relationship("Site", back_populates="feeds")
    code = Column(String(50), nullable=False)
    vendor_code = Column(String(255))
    type = Column(String(50))
    title = Column(String(255))
    subtitle = Column(String(255))
    link = Column(String(100), nullable=False)
    last_status = Column(Integer)
    response_last_modified = Column(String(100))
    response_etag = Column(String(100))
    updated = Column(DateTime(timezone=True))
    pinged = Column(DateTime(timezone=True))

    entries = relationship("Entry", back_populates="feed")

    def __repr__(self):
        return "<Feed(id='%d', code='%s', url='%s')>" % (int(self.id), self.code, self.link)

    def check(self):
        if self.link is None:
            return False

        if self.type == 'simple':
            print "Checking using method simple"
            feed = requests.get(self.link)
            self.pinged = func.now()
            self.last_status = feed.status_code
            print "Response: %d" % (feed.status_code)
            site_updated = False
            if feed.status_code == 200:
                if len(self.entries) > 0:
                    self.entries[0].pinged = func.now()
                    diff = difflib.Differ()
                    diff = list(diff.compare(feed.text.splitlines(), self.entries[0].content.splitlines()))
                    unchanged = 0
                    added = 0
                    removed = 0
                    for line in diff:
                        #print line
                        if line[0] == '+':
                            added += 1
                        if line[0] == '-':
                            removed += 1
                        if line[0] == ' ':
                            unchanged += 1
                    if unchanged == 0:
                        delta = 100
                    else:
                        delta = (float(added) / float(unchanged)) * 100
                    print "unchanged: %d, added: %d, removed: %d, delta: %f" % (unchanged, added, removed, delta)
                    if delta > 2:
                        self.entries[0].content = feed.text
                        site_updated = True
                    #print ''.join(diff),
                    print 
                    # only update entry and site if data is suffieciently different
                else:
                    temp_entry = Entry(vendor_code='cache',
                                        content=feed.text,
                                        pinged=func.now()
                                        )
                    self.entries.append(temp_entry)
                    site_updated = True
            if site_updated:
                self.updated = func.now()
        else:
            feed = feedparser.parse(self.link, modified=self.response_last_modified, etag=self.response_etag)
            self.pinged = func.now()
            self.last_status = feed.status
            print "Response: %d" % (feed.status)
            if feed.status == 200:
                # Now parse entries
                if self.title == self.code:
                    self.title = feed.feed.get('title', self.code)
                self.subtitle = feed.feed.get('subtitle', '')
                self.vendor_code = feed.feed.get('id', '')
                self.response_last_modified = feed.feed.get('modified', '')
                self.response_etag = feed.feed.get('etag', '')
                

                # this is probably wrong. Oh well...
                site_updated = False
                for feed_entry in feed.entries:

                    entry_exists = False
                    for child_entry in self.entries:
                        if child_entry.vendor_code == feed_entry.id:
                            entry_exists = True
                            break
                    if not entry_exists:
                        site_updated = True
                        content = ''
                        if 'content' in feed_entry:
                            if len(feed_entry.content):
                                content = feed_entry.content[0].value
                        temp_entry = Entry(vendor_code=feed_entry.get('id', ''),
                                           title=feed_entry.get('title', ''),
                                           link=feed_entry.get('link', ''),
                                           summary=feed_entry.get('summary', ''),
                                           content=content,
                                           author=feed_entry.get('author', ''),
                                           pinged=func.now()
                                           )
                        self.entries.append(temp_entry)
                if site_updated:
                    self.updated = func.now()



