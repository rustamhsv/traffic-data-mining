import pandas as pd
import tweepy

# twitter app settings
consumer_key = "yJ6jYKKHZjgleZZvxnw62TuyZ"
consumer_secret = "c6KZ1sIcbpVmZ79n2sXdKwX6lQ0SLiz1U9CDDlWeZTKlpdYlHq"
access_token = "1438393552241926146-F9swElHcab7JUr22iN5vFzC1joWLUN"
access_token_secret = "lVJFRfLdFXEps3cMLXsoskKRguetLREBY2CH8eIVIYHAT"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# request api
api = tweepy.API(auth)

# latitude, longitude, radius respectively
geocode = "47.497913,19.040236,50km"

# read keywords from excel file
keywords_df = pd.read_excel('hungarian_traffic_keywords.xlsx')
keywords_list = list(keywords_df['Keywords'])

# pandas dataframe to store dataframes for every keywords
tweets_df = []

# column headings for final dataframe
columns = ['Location', 'Username', 'Name', 'Date posted', 'Tweet', 'Retweet Count']

print('Searching for keywords:\n')
for keyword in keywords_list:
    print(keyword)

    # search for query/keyword in twitters posts [50km radius from Budapest center]
    tweets = api.search_tweets(q=keyword, geocode=geocode, result_type='mixed', count=100, tweet_mode='extended')

    # list to store instances of tweet data
    twitter_data = []
    for tweet in tweets:
        # get tweet location, username, name, date posted, tweet itself, and retweet count
        tweet_data = [tweet.geo, tweet.user.screen_name, tweet.user.name, tweet.created_at,
                      tweet.full_text, tweet.retweet_count]

        twitter_data.append(tweet_data)

    # create pandas dataframe out of twitter data
    df = pd.DataFrame(twitter_data, columns=columns)
    tweets_df.append(df)

# merge stored dataframes vertically
tweets_df = pd.concat(tweets_df, axis=0)

# write dataframe to csv
tweets_df.to_csv('Files/twitter_data_Budapest.csv')


# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)

# bearer_token = "AAAAAAAAAAAAAAAAAAAAALXLTwEAAAAAS2AhV3lwceGyUUGjCiuyLKPmSAk%3DOXwC5OC0SPbfK1HruuxNPqv3S3HzhM3TOK8Hv6fFe2ZqL3gVlQ"
