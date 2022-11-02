import tweepy as twitter
import keys

# print('this is my twitter bot')


# def api():
auth = twitter.OAuthHandler(keys.api_key, keys.api_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = twitter.API(auth)
    # return tweepy.API(auth)


# def tweet(api: tweepy.API, message: str, image_path=None):
#     if image_path:
#         api.update_status_with_media(message, image_path)
#     else:
#         api.update_status(message)


# print('Tweeted successfully')

# if __name__ == '__main__':
#     api = api()
#     tweet(api, 'Testing testing ')



def tweet(text):
  api.update_status(text)
  print('Tweeted successfully')

tweet("Hello this is a test tweet")
