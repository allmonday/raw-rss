# coding: utf-8

import feedparser as fp
import yaml
import json
import os
import sys
from pymongo import MongoClient

client = MongoClient()

if client['feeds'].authenticate('tangkikodo', 'feeds'):
    print('auth pass')
else:
    print('auth fail')

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

            print('log: link', link)
            print('log: author', ent['author'])

            # i dont know why, i need to skip 908961321
            if ent['author'] == '908961321':
                continue

            feedsdb.update({
                'author': ent['author'],
                'date': ent['date']
                }, ent, True)

    except Exception as e:
        print(e)

for b in blogs:
    getRss(b['link'])
