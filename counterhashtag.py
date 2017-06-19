# -*- coding: utf-8 -*-
"""Script used for SATToSE 17 Twitter competition

This script finds the tweets posted using #SATToSE17 hashtag
and calculates a score for each team taking into account the number
of retweets and favs of each tweet, and the number of team members who
are actively participating in the competition.

Tweets are stored at tweets.csv.

Usage:
        $ python counterhashtag.py

Todo:
    * After production use we realized that we should used user ids
    instead of user names to avoid cheating

"""

import csv
import math
from operator import truediv
import os
import twitter

#Data of the twitter app
api = twitter.Api(consumer_key="",
                  consumer_secret="",
                  access_token_key="",
                  access_token_secret="")

#Teams members
godzilla = ["Dorealda Dalipaj", "Alexander Serebrenik", "Mohammad Ghafari", "Alessandra Gorla",
            "Adrian Z.", "Nevena Milojkovic", "Alaaeddin Swidan", "Davide Spadini", "Julian",
            "Kim Mens", "Ali Parsai", "Alexandre Le Borgne", "Joost Visser"]
kingkong = ["Haidar Osman", "Tushar Sharma", "Andrei Chis", "Ward Muylaert", "Nick Lodewijks",
            "Yuriy Tymchuk", "Manuel Leuenberger", "Eleni Constantinou", "Luca Pascarella",
            "Marco di Biase", "Brent", "Felienne", "Tom Mens", "Vadim Zaytsev", "Daniel Izquierdo"]

#Read the previous list of tweets
with open('tweets.csv', 'rb') as csvfile:
    tweets = [{k: v for k, v in row.items()}
              for row in csv.DictReader(csvfile, skipinitialspace=True)]

ids = [row["id"] for row in tweets]

godzilla_active = []
kingkong_active = []
for row in tweets:
    if str(row["user"]) in godzilla:
        godzilla_active.append(row["user"])
    else: kingkong_active.append(row["user"])

#Get tweets using #SATToSE17
for s in api.GetSearch(raw_query="q=%23sattose17&count=100&result_type=recent"):
    in_competition = 0
    #Update lists of active users
    if s.user.name in godzilla:
        in_competition = 1
        if s.user.name not in godzilla_active:
            godzilla_active.append(s.user.name)
    elif s.user.name in kingkong:
        in_competition = 1
        if s.user.name not in kingkong_active:
            kingkong_active.append(s.user.name)
    #Update list of tweets with number of favs and retweets
    if in_competition:
        if str(s.id) in ids:
            tweets = [d for d in tweets if d['id'] != str(s.id)]
        tweets.append({"id" : s.id, "retweets" : s.retweet_count, "favs" : s.favorite_count,
                       "user" : s.user.name})

#Calculate scores
godzilla_points = 0
kingkong_points = 0

for t in tweets:
    if str(t["user"]) in godzilla:
        godzilla_points += 1 + float(t["retweets"]) + float(t["favs"])
    else:
        kingkong_points += 1 + float(t["retweets"]) + float(t["favs"])

godzilla_points = math.sqrt((godzilla_points * truediv(len(godzilla_active), len(godzilla))))
kingkong_points = math.sqrt((kingkong_points * truediv(len(kingkong_active), len(kingkong))))
print "Godzilla: " + str(round(godzilla_points, 2))
print "KingKong: " + str(round(kingkong_points, 2))

#Store the new list of tweets in tweets.csv
os.system("rm tweets.csv")

keys = tweets[0].keys()
with open('tweets.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys, quoting=csv.QUOTE_ALL)
    dict_writer.writeheader()
    dict_writer.writerows(tweets)
