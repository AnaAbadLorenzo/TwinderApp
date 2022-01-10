from twython import Twython
import requests
import tweepy
import json

consumer_key = 'k19hCICYf1ZGnB6kAZ48vF8DV'
consumer_secret = '3yR3QMHDoCqTYwpZ0LqciY6gKomnrZVbkLZuanvHQHfNpxWN5x'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAADvVWAEAAAAAruK0ce1DNbCERAlYQmJk0LfqgW8%3DaVQobIntKqgrjIjgGeaQzt32NDI8kvAKMsEduaMXRrlNEHkEh0'
access_token = '1464202275325366281-NW0O4qELIO5NVTzbfqvEKsPB3YbDV6'
access_token_secret = 'D5K9XAsZYx6anjvAhEEqHAiBn9dnPaGqQ81qsCWlsYjXv'
"""
auth = twitter.get_authentication_tokens(callback_url='http://mysite.com/callback')
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

auth['auth_url']
"""

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)
tweepy_api = tweepy.API(auth)

def getuser(user):
    return listarTweets(user)

def listarTweets (userID):
    toret = list()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=userID,
                               # 200 is the maximum allowed count
                               count=200,
                               include_rts = False,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
    ctr=0
    for info in tweets:
        ctr+=1
        print("ID: {0}. Num tweet {1}".format(info.id, ctr))
        print("Created at: {}".format(info.created_at))
        print("Texto: {}".format(info.full_text))
        print("\n")
        toret.append(info.full_text)
    return toret

# twitter = Twython(consumer_key, access_token=access_token)
# print(ACCESS_TOKEN)
#
# print(twitter.search(q='python'))
# dict = twitter.search(q='python')

# def get_tweets(username):
#     tweets = tweepy_api.user_timeline(screen_name=username)
#     return [{’tweet’: t.text,'created_at’: t.created_at,'username’: username,'headshot_url’: t.user.profile_image_url}
#     for t in tweets]

def search_twitter(query, tweet_fields, bearer_token = BEARER_TOKEN):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}

    url = "https://api.twitter.com/2/tweets/search/recent?query={0}&{0}".format(query, tweet_fields)
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


query = "dog"
tweet_fields = "text,author_id,created_at"

#saved = search_twitter(query,tweet_fields,bearer_token=BEARER_TOKEN)

