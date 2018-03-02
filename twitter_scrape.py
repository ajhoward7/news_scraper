import sys
import tweepy
import yaml


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


def fetch_tweets(api, name, n=20):
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

        tweet = {'id':id, 'created':created, 'text':text, 'hashtags':hashtags, 'urls':urls, 'mentions':mentions}

        tweets.append(tweet)

    return {'user':name, 'count':n, 'tweets':tweets}


def load_configs(path = 'conf/confs.yaml'):
    # Load configurations.yaml file
    CONFS = yaml.load(open(path))
    return CONFS

def get_conf(conf_name):
    # Load specific configuration from configurations file
    return load_configs()[conf_name]

if __name__ == "__main__":
    # Putting auxillary functions together and writing output to file

    twitter_creds_file = sys.argv[1]
    try:
        output_filename = sys.argv[2]
    except:
        output_filename = 'output.txt'

    api = authenticate(twitter_creds_file)
    users = get_conf("twitter_handles")
    f = open(output_filename,'w')

    try:
        n = get_conf("n")
    except:
        n = 20
        print "No 'n' specified -- using default value of 20 most recent tweets"

    for user in users:
        f.write(str(fetch_tweets(api,user,n)) + '\n\n')
        print "Written tweets for {}".format(user)

    print "Completed Analysis, output is in {}".format(output_filename)
