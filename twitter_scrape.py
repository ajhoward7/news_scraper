import sys
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def loadkeys(filename):
    """"
    load twitter api keys/tokens from CSV file with form
    consumer_key, consumer_secret, access_token, access_token_secret
    """
    with open(filename) as f:
        items = f.readline().strip().split(', ')
        return items


def authenticate(twitter_auth_filename):
    """
    Given a file name containing the Twitter keys and tokens,
    create and return a tweepy API object.
    """
    consumer_key, consumer_secret, \
    access_token, access_token_secret \
        = loadkeys(twitter_auth_filename)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def fetch_tweets(api, name, n):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    create a list of tweets where each tweet is a dictionary with the
    following keys:

       id: tweet ID
       created: tweet creation date
       retweeted: number of retweets
       text: text of the tweet
       hashtags: list of hashtags mentioned in the tweet
       urls: list of URLs mentioned in the tweet
       mentions: list of screen names mentioned in the tweet
       score: the "compound" polarity score from vader's polarity_scores()

    Return a dictionary containing keys-value pairs:

       user: user's screen name
       count: number of tweets
       tweets: list of tweets, each tweet is a dictionary

    For efficiency, create a single Vader SentimentIntensityAnalyzer()
    per call to this function, not per tweet.

    Note: additional argument n added to specify number of tweets to fetch
    """
    user_tweets = []

    for status in tweepy.Cursor(api.user_timeline, id=name).items(n):
        user_tweets.append(status)

    tweets = []

    for i in range(n):
        user_tweet_i = user_tweets[i]
        id = user_tweet_i.id
        created = user_tweet_i.created_at
        text = user_tweet_i.text
        hashtags = user_tweet_i.entities['hashtags']
        urls = user_tweet_i.entities['urls']
        mentions = user_tweet_i.entities['user_mentions']

        analyzer = SentimentIntensityAnalyzer()
        sentimentscore = analyzer.polarity_scores(text)['compound']

        tweet = {'id':id, 'created':created, 'text':text, 'hashtags':hashtags, 'urls':urls, 'mentions':mentions, 'score':sentimentscore}

        tweets.append(tweet)

    return {'user':name, 'count':n, 'tweets':tweets}



def fetch_following(api,name):
    """
    Given a tweepy API object and the screen name of the Twitter user,
    return a a list of dictionaries containing the followed user info
    with keys-value pairs:

       name: real name
       screen_name: Twitter screen name
       followers: number of followers
       created: created date (no time info)
       image: the URL of the profile's image

    To collect data: get a list of "friends IDs" then get
    the list of users for each of those.
    """
    following = []
    # num_friends = api.get_user(name).friends_count
    for friend in tweepy.Cursor(api.friends, id=name, count = 200).items():
        real_name = friend.name
        screen_name = friend.screen_name
        followers = friend.followers_count
        created = friend.created_at.date()
        image_url = friend.profile_image_url
        my_dict = {'name':real_name, 'screen_name':screen_name, 'followers':followers, 'created':created, 'image':image_url}
        following.append(my_dict)

    return following
