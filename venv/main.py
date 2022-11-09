import tweepy as twitter
import requests
import asyncio
import time
import json
import keys
import re

city = ''
aqual = None

def get_data():
    new_data = None
    response = requests.get(
        f'http://api.waqi.info/feed/{city}/?token={keys.API_TOKEN}')
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


hold = []

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
        (f'@{mention.user.screen_name} Air Quality Index in {city} is currently {aqual} '), mention.id)
    print('Replied to @ ' + mention.user.screen_name)

  last_seen_id = retrieve_id(FILE)
  mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

  for mention in reversed(mentions):
  # hold = mentions[1]._json['id']
  # if hold!= None:
  #     print(hold, 'hold here')
    # if mention._json['id'] == last_seen_id:
    #   print(mention._json['id'], last_seen_id)
    #   break
    # else:
      # hold.append((mention._json['id']))
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
        aqual = get_data()
        print(aqual, 'aqual here')
        # if aqual:
        reply()

    

  print("sleeping")
  time.sleep(10)
  print('awake')