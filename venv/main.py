

import tweepy as twitter
import requests
import asyncio
import time
import json
import keys
import re

city = ''
aqual = None
error_msg = None

def get_data():
    new_data = None
    response = requests.get(
        f'http://api.waqi.info/feed/{city}/?token={keys.API_TOKEN}')
    data = response.text
    parse_json = json.loads(data)
    # print(parse_json['status'], 'here')
    if parse_json['status'] == 'error':
      err_reply()
    elif parse_json['status'] == 'ok':
      for key in parse_json.keys():
        if key == 'data':
            new_data = (key, parse_json[key])
            aqual = new_data[1]['aqi']
            return aqual

            
auth = twitter.OAuthHandler(keys.api_key, keys.api_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = twitter.API(auth, wait_on_rate_limit=True)

FILE = "id.txt"

while True:
  def retrieve_id(file):
    f_read = open(file, "r")
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id

  def store_id(id, file):
    f_write = open(file, "w")
    f_write.write(str(id))
    f_write.close()
    return

  def reply():
    api.update_status(
        (f'@{mention.user.screen_name} PM2.5 Air Quality Index in {city} is currently {aqual} '), mention.id)
    print('Replied to @ ' + mention.user.screen_name)

  def err_reply():
    print('there was an error')
    api.update_status(
        (f'@{mention.user.screen_name} It seems there was touble retrieving data for the city of {city} '), mention.id)
    print('Replied to @ ' + mention.user.screen_name)

  last_seen_id = retrieve_id(FILE)
  mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

  for mention in reversed(mentions):
      if "airqual" in mention.full_text:
        last_seen_id = mention.id
        store_id(last_seen_id, FILE)
        tweet = (mention.full_text)
        clean_tweet = re.sub("@[A-Za-z0-9_]+", "", tweet)
        clean_tweet = re.sub("#[A-Za-z0-9_]+", "", clean_tweet)
        clean_tweet = re.sub("''[A-Za-z0-9_]+", "", clean_tweet)
        clean_tweet = clean_tweet.lower()
        clean_tweet = clean_tweet.replace(" ", "")
        clean_tweet = " ".join(clean_tweet.split())
        # logic to sort location for api search params go here
        city = clean_tweet
        print(city)
        # logic for conditional rendering of error msg or aqual here
        aqual = get_data()
        if aqual != None:
          print(f'{aqual} for {city}')
          reply()
        

  print("sleeping")
  time.sleep(30)
  print('awake')