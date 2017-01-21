#!/usr/bin/env python
import yaml
import os.path
from shutil import copy
from linkchecker import *
import MySQLdb
from sqlalchemy import create_engine




if not os.path.isfile("config.local.yaml"):
    print "Could not locate config.local.yaml. Going to create one from config.yaml..."
    copy("./config.yaml", "./config.local.yaml")

if not os.path.isfile("init.local.yaml"):
    print "Could not locate init.local.yaml. Going to create one from init.yaml..."
    copy("./init.yaml", "./init.local.yaml")


with open("config.local.yaml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit()


with open("init.local.yaml", 'r') as stream:
    try:
        init = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit()

# create an engine for the LinkChecker to work against
engine = create_engine(config['config']['connection_string'], echo=False)

# TODO: do something to construct db agnostic connection string from configs
lc = LinkChecker(engine, init)

lc.check_all()

print
print
print
#print lc.test_output_simple()

# bluh = Site()
# bluh.code = "fdsafas"
# bluh.get_by_code("fdsafas");


# print "Let's test some feeds:"
# for code, site in config['sites'].iteritems():
#     print "[%s] %s" % (code, site['name']) 
#     if site['type'] != 'no-rss':
#         for url in site['urls']:
#             print url
#             feed = feedparser.parse(url)
#             print feed
#     else:
#         "This site not configured for rss."
#     print
