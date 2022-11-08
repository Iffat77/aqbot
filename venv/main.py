import tweepy as twitter
import requests 
import asyncio
import time
import json
import keys
import re

# async def main():
#   print('heres johnny')
#   await foo('text')

# async def foo(text):
#   print(text)
#   await asyncio.sleep(1)


# asyncio.run(main())

city = ''
aqual = None

def get_data():
  new_data = None
  response = requests.get(f'http://api.waqi.info/feed/{city}/?token={keys.API_TOKEN}')
  data = response.text
  parse_json = json.loads(data)
  for key in parse_json.keys():
    if key == 'data':
      new_data = (key, parse_json[key])
      aqual = new_data[1]['aqi']
      print(aqual) 
      return aqual   
    



auth = twitter.OAuthHandler(keys.api_key, keys.api_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = twitter.API(auth)

FILE = "id.txt"

def retrieve_id(file):
  f_read=open(file, "r")
  last_seen_id = int(f_read.read().strip())
  f_read.close()
  return last_seen_id

def store_id(id, file):
  f_write = open(file, "w")
  f_write.write(str(id))
  f_write.close()
  return

def reply():
  api.update_status((f'@{mention.user.screen_name} Air Quality Index in {city} is currently {aqual} '), mention.id)
      # api.update_status('@'+mention.user.screen_name + ' '+ city + ' air quality is currently '+ aqual ' ' , mention.id)
  print('Replied to @ ' + mention.user.screen_name)

last_seen_id = retrieve_id(FILE)
mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

for mention in reversed(mentions):
    if "airqual" in mention.full_text:
      tweet = (mention.full_text)
      # print(tweet, "printing tweet")
      clean_tweet = re.sub("@[A-Za-z0-9_]+","", tweet)
      # print(clean_tweet, "this is clean tweet no @")
      clean_tweet = re.sub("#[A-Za-z0-9_]+","", clean_tweet)
      # print(clean_tweet, "clean tweet no @ or #")
      clean_tweet = re.sub("''[A-Za-z0-9_]+","", clean_tweet)
      clean_tweet = clean_tweet.lower()
      clean_tweet = clean_tweet.replace(" ", "")
      clean_tweet = " ".join(clean_tweet.split())
      # print(clean_tweet, "this is the clean tweet")
      # logic to sort location for api search params go here
      city = clean_tweet
      print(city)
      aqual = get_data()
      print(aqual, 'here')
      last_seen_id = mention.id
      store_id(last_seen_id, FILE)
      reply()
      

# get_data function 
# reply function
# make for loop for mentions a function
'''
import requests
from requests_oauthlib import OAuth1
import os
'''