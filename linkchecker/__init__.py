from sqlalchemy.orm import sessionmaker
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

from site import Site
from feed import Feed
from entry import Entry


__all__ = ["Entry", "Feed", "Site", "LinkChecker", "Base"]


# Create DB schema.



class LinkChecker:

    def __init__(self, engine, init):
        self.db = engine
        self.init = init

        try:
            self.db.connect()
        except sqlalchemy.exc.OperationalError:
            # Could not connect to database. This needs to be fixed
            # outside of this script.
            print "Error. Could not connect to database. Please fix connection and try again."
            exit()

        # Verify that we have tables and create if necessary.
        Base.metadata.create_all(self.db)

        self.Session = sessionmaker(bind=self.db)
        self.session = self.Session()

        # Count the sites in the current db to see if we need to initialize.
        site_rows = self.session.query(Site).count()
        if (site_rows == 0):
            self.initialize_data()


    def initialize_data(self):
        print self.init
        print

        print "Initializing data"
        for code, site in self.init['init'].iteritems():
            temp_title = code
            if 'title' in site:
                temp_title = site['title']
            temp_link = ''
            if 'link' in site:
                temp_link = site['link']
            temp_tags = ''
            if 'tags' in site:
                temp_tags = json.dumps(site['tags'])
            temp_site = Site(code=code, title=temp_title, link=temp_link, tags=temp_tags)
            self.session.add(temp_site)
            self.session.commit()

            for feedcode, feed in site['feeds'].iteritems():
                temp_name = feedcode
                if 'title' in feed:
                    temp_name = feed['title']
                temp_type = 'rss'
                if 'type' in feed:
                    temp_type = feed['type']
                temp_feed = Feed(site_id=temp_site.id, code=feedcode, title=temp_name, link=feed['link'], type=temp_type)
                self.session.add(temp_feed)
                self.session.commit()


            print temp_site;


    def check_all(self):
        print "Checking all sites..."
        sites = self.session.query(Site)

        for site in sites:
            for feed in site.feeds:
                print "%s: %s => %s" % (site.title, feed.code, feed.link)
                feed.check()
                self.session.commit()





#     print "[%s] %s" % (code, site['name']) 
#     if site['type'] != 'no-rss':
#         for url in site['urls']:
#             print url
#             feed = feedparser.parse(url)
#             print feed
#     else:
#         "This site not configured for rss."
#     print


