#coding: utf-8
# for python 2.7

import feedparser as fp
import yaml
import json
import os,sys
from pymongo import MongoClient

client = MongoClient()
feedsdb = client['feeds'].entries

currentDir = os.path.dirname(os.path.realpath(__file__))
bloglist = currentDir + "/blogs.yml"

try:
    blogs = yaml.load(open(bloglist))
except Exception as e:
    print(e)
print('start work')

blogs = blogs['blogs']

def getRss(link):
    print('doing->', link)
    try:
        f = fp.parse(link)
        entries = []
        for e in f.entries:
            ent = {
                'title': e.title_detail.value,
                'author': e.author_detail.name,
                'link': e.id,
                'date': ' '.join(e.published.split(' ')[1:4])
                }
                
            # upsert record
            feedsdb.update({
                'author': ent['author'],
                'date': ent['date']
                }, ent, True)
            
    except Exception as e:
        print(e)
    return entries

all_blogs = []

for b in blogs:
    all_blogs.extend(getRss(b['link']))
