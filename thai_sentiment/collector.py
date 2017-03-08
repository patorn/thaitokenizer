import os
import json
import time

import tweepy

REPO_DIR = os.getenv('data', '.')
RAW_PATH = '{0}/data/raw'.format(REPO_DIR)

os.makedirs(RAW_PATH, exist_ok=True)

if __name__ == '__main__':

    with open('config.json','r') as file:
        config = json.load(file)

    auth = tweepy.AppAuthHandler(config['consumer_key'], config['consumer_secret'])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    tweet_count = 0
    sentiment_label = ":) -filter:retweets"

    #max_id

    for tweet in tweepy.Cursor(api.search, q=sentiment_label, lang='th', count=100).items(1000):
        tweet = tweet._json
        result =  {
            "id": tweet['id'],
            "user_id": tweet['user']['id'],
            "text": tweet['text'],
            "created_at": tweet['created_at'],
            "sentiment": sentiment_label,
        }

        with open(RAW_PATH + '/' + str(result['id']) + '.json', 'w', encoding='utf-8') as file:
            json.dump(result, file, indent=4, ensure_ascii=False)

        tweet_count += 1

        if tweet_count % 1000 == 0:
            print("Downloaded {0} tweets".format(tweet_count))

    #Display how many tweets we have collected
    print("Downloaded {0} tweets".format(tweet_count))
    print(api.rate_limit_status()['resources']['search'])
