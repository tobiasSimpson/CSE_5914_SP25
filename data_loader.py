import csv
import json
import pandas as pd
from tqdm import tqdm

DATA_FOLDER = 'data'

# load tweets from sanders dataset
def load_sanders_tweets(filename: str, silent: bool) -> pd.DataFrame:
    # Create file names for csv and json files
    csvFilePath = f"{DATA_FOLDER}/{filename}.csv"
    jsonFilePath = f"{DATA_FOLDER}/{filename}.json"

    # Open the csv file
    column_names = ["topic", "sentiment", "tweet_id", "date", "text"]
    tweets = pd.read_csv(csvFilePath, header=None, names=column_names)
    tweets.dropna(inplace=True)

    return tweets

def load_celebrity_tweets(filename: str) -> pd.DataFrame:
    column_names = ['user', 'sentiment', 'text']
    tweets = pd.read_csv(f'{DATA_FOLDER}/{filename}.csv', header=None, names=column_names)
    tweets.dropna(inplace=True)
    return tweets

def load_cikm_tweets(filename: str, silent: bool):
    # helper to process a single file line
    def process_line(line):
        parts = line.strip().split('\t')
        if len(parts) != 4:
            return None
        user_id, tweet_id, tweet, created_at = parts
        return parts

    # Create tweet list to add to
    tweets = list()

    # Create file names for csv and json files
    txtFilePath = f"{DATA_FOLDER}/{filename}.txt"
    jsonFilePath = f"{DATA_FOLDER}/{filename}.json"

    # Open the csv file
    with open(txtFilePath, encoding="utf8") as file:
        for line in tqdm(file):
            # Process each row as a tweet
            line = process_line(line)
            if line:
                # Create dict for tweet
                tweet = dict()

                # Add each tweet element to dict
                tweet['user_ID'] = line[0]
                tweet['tweet_ID'] = line[1]
                tweet['text'] = line[2]
                tweet['date'] = line[3]

                # Add tweet to list of tweets
                tweets.append(tweet)
    # Clear json file
    open(jsonFilePath, 'w').close()
    # Open json file
    with open(jsonFilePath, "w") as file:
        # Dump tweets into json
        file.write(json.dumps(tweets))

def load_data():
    sander_tweets = load_sanders_tweets('sanders_corpus', False)
    celeb_tweets = load_celebrity_tweets('celebrity_tweets')
    #load_cikm_tweets('cikm_2010_tweets', False)
    data = pd.concat([sander_tweets, celeb_tweets], ignore_index=True, sort=False)
    print(data.head())
    data.to_json(f"{DATA_FOLDER}/data.json", orient='records')

if __name__ == '__main__':
    load_data()
