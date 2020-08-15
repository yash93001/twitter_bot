import tweepy, logging
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def display_greet():
    print('WELCOME')
    print('~~~~~~~')
    print('I am an Auto-Liker Bot')


def disp_index():

    print('What Can I Do For You')
    print('1> Like tweet of specific user and with specific hashtags\n',
          '2> Like tweets with given hashtags with different unique\n',
          '3> Like tweets with given hashtags\n','Enter your choice (1,2,3)')

    task_choice = int(input())

    print('Enter Hashtags (Seperate them with ,)')
    hashtag_list = list(map(str, input().split(',')))

    for i in range(len(hashtag_list)):
        hashtag_list[i] = hashtag_list[i].strip()
        if hashtag_list[i][0] != '#':
            hashtag_list[i] = '#' + hashtag_list[i]

    if task_choice == 1:
        print('Enter the specific username/screenname that you want to look-up for')
        user_name = input().strip()
        print('Enter the max number of post to be liked (if all enter 0)')
        count = int(input())

    else:
        user_name = ''
        print('Enter the time duration for which you want tweets to be liked.(Enter in secs)')
        count = int(input())
    return hashtag_list, user_name, task_choice, count


def authenticate_api():
    
    consumer_key = 'Should Be stored as enviornment variable'
    consumer_secret = 'Should Be stored as enviornment variable'
    access_token = 'Should Be stored as enviornment variable'
    access_secret = 'Should Be stored as enviornment variable'

    # authenticate to twitter api
    logger = logging.getLogger()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def specific_user_no_of_tweets(api, keyword, user, count):
    tweet_list = api.user_timeline(screen_name=str(user), count=9999)
    for tweets in tweet_list:
        if(count == 0):
            break
        if not tweets.favorited:
            texts = tweets.text
            text_lines = list(map(str,texts.split('\n')))
            d_words = {}
            for each_line in text_lines:
                t = list(map(str,each_line.split(' ')))
                for i in t:
                    d_words[i] = 1
            flag = 0
            for words in keyword:
                if not d_words.get(words,):
                    flag = 1
                    break
            if(flag == 0):
                tweets.favorite()
                count -=1



def random_user_tweet_likes(api,keywords,runtime):
    tweets_listener = twitter_like(api,runtime)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track= keywords)


def unique_user_tweet_likes(api,keywords,runtime):
    print(keywords,runtime)
    tweets_listener = twitter_like_random(api,runtime)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track= keywords)


class twitter_like_random(tweepy.StreamListener):
    def __init__(self, api, runtime):
        self.api = api
        self.me = api.me()
        self.start_time = time.time()
        self.limit = runtime

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if (time.time() - self.start_time) < self.limit:

            if not tweet.favorited:
                try:
                    tweet.favorite()
                except Exception as e:
                    logger.error("Error on fav", exc_info=True)
        else:
            return False

    def on_error(self, status):
        logger.error(status)


class twitter_like(tweepy.StreamListener):
    def __init__(self, api,runtime):
        self.api = api
        self.me = api.me()
        # dict will store all userid used
        self.d = {}
        self.start_time = time.time()
        self.limit = runtime

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if (time.time() - self.start_time) < self.limit:
            if not self.d.get(tweet.user.id,):
                self.d[tweet.user.id] = 1
                if not tweet.favorited:
                    try:
                        tweet.favorite()
                    except Exception as e:
                        logger.error("Error on fav", exc_info=True)
        else:
            return False

    def on_error(self, status):
        logger.error(status)

def disp_quit():
    print('Press 1 to search again')
    print('Press 0 to Exit')
    t = int(input())
    return t
