#'''
#tweetDAta=>600

import asyncio
from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 600
DATE_RANGES = [
    ("2018-01-01", "2019-01-01"),
    ("2019-01-01", "2020-01-01"),
    ("2020-01-01", "2021-01-01"),
    ("2021-01-01", "2022-01-01"),
    ("2022-01-01", "2023-01-01"),
    ("2023-01-01", "2024-01-01"),
]

async def get_tweets(tweets, client, query):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets for query: {query}')
        tweets = await client.search_tweet(query, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets

async def main():
    config = ConfigParser()
    config.read('config.ini')

    try:
        username = config['X']['username']
        email = config['X']['email']
        password = config['X']['password']
    except KeyError as e:
        raise KeyError(f"Missing key in 'config.ini': {e}")

    with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    client = Client(language='en-US')
    await client.login(auth_info_1=username, auth_info_2=email, password=password)

    tweet_count = 0

    for since_date, until_date in DATE_RANGES:
        query = f'(from:elonmusk) lang:en until:{until_date} since:{since_date}'
        tweets = None

        while tweet_count < MINIMUM_TWEETS:
            try:
                tweets = await get_tweets(tweets, client, query)
            except TooManyRequests as e:
                rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset) if e.rate_limit_reset else None
                wait_time = (rate_limit_reset - datetime.now()).total_seconds() if rate_limit_reset else 15 * 60
                print(f'{datetime.now()} - Rate limit reached. Waiting for {wait_time:.2f} seconds...')
                await asyncio.sleep(wait_time)
                continue
            except Exception as e:
                print(f'{datetime.now()} - Unexpected error: {e}')
                break

            if not tweets:
                print(f'{datetime.now()} - No more tweets found for query: {query}')
                break

            for tweet in tweets:
                tweet_count += 1
                tweet_data = [
                    tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count
                ]
                with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(tweet_data)

                if tweet_count >= MINIMUM_TWEETS:
                    break

            print(f'{datetime.now()} - Got {tweet_count} tweets')

        if tweet_count >= MINIMUM_TWEETS:
            break

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets')

if __name__ == "__main__":
    asyncio.run(main())

#'''

'''
#tweetData=>92 optimized

import asyncio
from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 600
QUERY = '(from:elonmusk) lang:en until:2024-01-01 since:2018-01-01'

async def get_tweets(tweets, client):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets

async def main():
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    client = Client(language='en-US')
    await client.login(auth_info_1=username, auth_info_2=email, password=password)

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets, client)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset) if e.rate_limit_reset else None
            if rate_limit_reset:
                wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            else:
                wait_time = 15 * 60
            print(f'{datetime.now()} - Rate limit reached. Waiting for {wait_time} seconds...')
            await asyncio.sleep(wait_time)
            continue
        except Exception as e:
            print(f'{datetime.now()} - Unexpected error: {e}')
            break

        if not tweets:
            print(f'{datetime.now()} - No more tweets found.')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
            with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets')

if __name__ == "__main__":
    asyncio.run(main())

'''


'''
#tweeterData=>20-92
import asyncio
from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 600
QUERY = '(from:elonmusk) lang:en until:2024-01-01 since:2018-01-01'
#QUERY = '(from:elonmusk) lang:en until:2024-01-01 since:2020-01-01'

async def get_tweets(tweets, client):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()

    return tweets

async def main():
    #* login credentials
    config = ConfigParser()
    config.read('config.ini')
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']

    #* create a csv file
    with open('tweets.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])

    #* authenticate to X.com
    client = Client(language='en-US')
    
    # Await the login method to properly handle asynchronous login
    await client.login(auth_info_1=username, auth_info_2=email, password=password)

    tweet_count = 0
    tweets = None

    while tweet_count < MINIMUM_TWEETS:
        try:
            tweets = await get_tweets(tweets, client)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = (rate_limit_reset - datetime.now()).total_seconds()
            await asyncio.sleep(wait_time)
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]

            with open('tweets.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(tweet_data)

        print(f'{datetime.now()} - Got {tweet_count} tweets')

    print(f'{datetime.now()} - Done! Got {tweet_count} tweets')

if __name__ == "__main__":
    asyncio.run(main())


'''











"""
from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint


MINIMUM_TWEETS = 10
QUERY = '(from:elonmusk) lang:en until:2020-01-01 since:2018-01-01'
#QUERY = '(from:elonmusk) lang:en until:2024-01-01 since:2020-01-01'


def get_tweets(tweets):
    if tweets is None:
        #* get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        time.sleep(wait_time)
        tweets = tweets.next()

    return tweets


#* login credentials
config = ConfigParser()
config.read('config.ini')
username = config['X']['username']
email = config['X']['email']
password = config['X']['password']

#* create a csv file
with open('tweets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Tweet_count', 'Username', 'Text', 'Created At', 'Retweets', 'Likes'])



#* authenticate to X.com
#! 1) use the login credentials. 2) use cookies.
client = Client(language='en-US')
# client.login(auth_info_1=username, auth_info_2=email, password=password)
# client.save_cookies('cookies.json')

client.load_cookies('cookies.json')

tweet_count = 0
tweets = None

while tweet_count < MINIMUM_TWEETS:

    try:
        tweets = get_tweets(tweets)
    except TooManyRequests as e:
        rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
        print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
        wait_time = rate_limit_reset - datetime.now()
        time.sleep(wait_time.total_seconds())
        continue

    if not tweets:
        print(f'{datetime.now()} - No more tweets found')
        break

    for tweet in tweets:
        tweet_count += 1
        tweet_data = [tweet_count, tweet.user.name, tweet.text, tweet.created_at, tweet.retweet_count, tweet.favorite_count]
        
        with open('tweets.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(tweet_data)

    print(f'{datetime.now()} - Got {tweet_count} tweets')


print(f'{datetime.now()} - Done! Got {tweet_count} tweets found')
"""




'''

from twikit import Client, TooManyRequests
import time
from datetime import datetime
import csv
from configparser import ConfigParser
from random import randint

MINIMUM_TWEETS = 10
QUERY = 'chatgpt'

#* Load login credentials from config file
config = ConfigParser()
config.read('config.ini')

try:
    username = config['X']['username']
    email = config['X']['email']
    password = config['X']['password']
except KeyError as e:
    raise KeyError(f"Missing key in 'config.ini': {e}")

#* Authenticate to X.com
client = Client(language='en-US')

try:
    client.login(auth_info_1=username, auth_info_2=email, password=password)
    client.save_cookies('cookies.json')
    print("Login successful. Cookies saved to 'cookies.json'.")
except TooManyRequests:
    print("Too many requests. Please try again later.")
except Exception as e:
    print(f"An error occurred: {e}")

    
'''