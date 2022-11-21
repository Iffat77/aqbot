import tweepy 
import requests
import asyncio
import time
import json
import keys
import re

city = ''
aqual = None
error_msg = None

while True:
  def get_data():
    new_data = None
    response = requests.get(
        f'http://api.waqi.info/feed/{city}/?token={keys.API_TOKEN}')
    data = response.text
    parse_json = json.loads(data)
    if parse_json['status'] == 'error':
      err_reply()
    elif parse_json['status'] == 'ok':
      for key in parse_json.keys():
        if key == 'data':
            new_data = (key, parse_json[key])
            aqual = new_data[1]['aqi']
            return aqual

  client = tweepy.Client(keys.bearer_token, keys.api_key, keys.api_secret, keys.access_token, keys.access_token_secret)
  auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret)
  auth.set_access_token(keys.access_token, keys.access_token_secret)
  api = tweepy.API(auth)

  client_id = client.get_me().data.id
  start_id = None
  
  def err_reply():
    print('there was an error')
    api.update_status(
        (f'@{mention.user.screen_name} It seems there was touble retrieving data for the city of {city} '), mention.id)
    print('Replied to @ ' + mention.user.screen_name)


  res = client.get_users_mentions(client_id, since_id=start_id)

  if res.data != None:
    for twee in res.data:
      print(start_id, 'first id')
      twee_id = res.meta['newest_id']
      mention = (str(twee))
      if 'airqual' in mention:
        tweet = mention
        clean_tweet = re.sub("@[A-Za-z0-9_]+", "", tweet)
        clean_tweet = re.sub("#[A-Za-z0-9_]+", "", clean_tweet)
        clean_tweet = re.sub("''[A-Za-z0-9_]+", "", clean_tweet)
        clean_tweet = clean_tweet.lower()
        clean_tweet = clean_tweet.replace(" ", "")
        clean_tweet = " ".join(clean_tweet.split())
        city = clean_tweet
        aqual = get_data()
      if aqual != None:
        message = (f'PM2.5 Air Quality Index in {city} is currently {aqual}') 
        try:
          print(city, 'here')
          print(message)
          client.create_tweet(in_reply_to_tweet_id=twee_id, text=message)
          start_id = twee_id
          print(start_id, 'new id')
        except Exception as error:
          print(error)

  print("sleeping")
  time.sleep(30)
  print('awake')


