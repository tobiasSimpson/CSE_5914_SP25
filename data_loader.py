import csv
import json
from tqdm import tqdm

DATA_FOLDER = 'data'

# load tweets from sanders dataset
def load_sanders_tweets(filename: str):
    # Create tweet list to add to
    tweets = list()

    # Create file names for csv and json files
    csvFilePath = f"{DATA_FOLDER}/{filename}.csv"
    jsonFilePath = f"{DATA_FOLDER}/{filename}.json"

    # Open the csv file
    with open(csvFilePath, encoding='utf-8') as file:
        # Read csv as dict
        csvReader = csv.DictReader(file)

        # Process each row as a tweet
        for row in tqdm(csvReader):
            # Create dict for tweet
            tweet = dict()

            # Add each tweet element to dict
            tweet['topic'] = row['Topic']
            tweet['sentiment'] = row['Sentiment']
            tweet['ID'] = row['TweetId']
            tweet['date'] = row['TweetDate']
            tweet['text'] = row['TweetText']

            # Add tweet to list of tweets
            tweets.append(tweet)
    # Clear json file
    open(jsonFilePath, 'w').close()
    # Open json file
    with open(jsonFilePath, "w") as file:
        # Dump tweets into json
        file.write(json.dumps(tweets))


# load tweets from celebrities
def load_celebrity_tweets(filename: str):
    # Create tweet list to add to
    tweets = list()

    # Create file names for csv and json files
    csvFilePath = f"{DATA_FOLDER}/{filename}.csv"
    jsonFilePath = f"{DATA_FOLDER}/{filename}.json"

    # Open the csv file
    with open(csvFilePath, encoding='utf-8') as file:
        # Read csv as dict
        csvReader = csv.reader(file)

        # Process each row as a tweet
        for row in tqdm(csvReader):
            # Create dict for tweet
            tweet = dict()

            # Add each tweet element to dict
            tweet['author'] = row[0]
            tweet['sentiment'] = row[2]
            tweet['text'] = row[1]

            # Add tweet to list of tweets
            tweets.append(tweet)
    # Clear json file
    open(jsonFilePath, 'w').close()
    # Open json file
    with open(jsonFilePath, "w") as file:
        # Dump tweets into json
        file.write(json.dumps(tweets))

def load_cikm_tweets(filename: str):
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
    load_sanders_tweets('sanders_corpus')
    load_celebrity_tweets('celebrity_tweets_results')
    load_cikm_tweets('cikm_2010_tweets')

if __name__ == '__main__':
    load_data()
