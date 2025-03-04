import pandas as pd
from tqdm import tqdm

DATA_FOLDER = 'data'

# load tweets from sanders dataset
def load_sanders_tweets(filename: str = 'sanders_corpus.csv') -> pd.DataFrame:
    filepath = f"{DATA_FOLDER}/{filename}"
    df = pd.read_csv(filepath)
    df.drop(columns=['TweetId', 'Sentiment'], inplace=True)
    df.dropna(inplace=True)
    df['TweetDate'] = pd.to_datetime(df['TweetDate'])
    return df

# load tweets from celebrities
def load_celebrity_tweets(filename: str = 'celebrity_tweets.csv') -> pd.DataFrame:
    column_names = ['user', 'tweet', 'sentiment_label']
    df = pd.read_csv(f'{DATA_FOLDER}/{filename}', header=None, names=column_names)
    # drop sentiment column:
    df.drop(columns=['sentiment_label'], inplace=True)
    df.dropna(inplace=True)
    return df

# load trump tweets dataset
def load_trump_tweets(filename: str) -> pd.DataFrame:
    column_names = ['text', 'favorites', 'retweets', 'date']
    tweets = pd.read_csv(f'{DATA_FOLDER}/{filename}.csv', usecols=column_names)
    tweets.dropna(inplace=True)
    return tweets

def load_cikm_tweets(filename: str = 'cikm_2010_tweets.txt') -> pd.DataFrame:
    # helper to process a single file line
    def process_line(line):
        parts = line.strip().split('\t')
        if len(parts) != 4:
            return None
        user_id, tweet_id, tweet, created_at = parts
        # return {'Tweet': tweet, 'CreatedAt': created_at}
        return (tweet, created_at)
    
    # read file and process each line:
    file_lines = open(f'{DATA_FOLDER}/{filename}').readlines()
    results = []
    for line in tqdm(file_lines):
        result = process_line(line)
        if result:results.append(result)
    
    df = pd.DataFrame(results, columns=['Tweet', 'CreatedAt'])
    # read created at column as datetime, and drop any row with invalid values:
    df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], errors='coerce')
    df.dropna(inplace=True)
    return df


def debug():
    print(f'testing tweet file loading...')
    df = load_celebrity_tweets()
    print(f'Celebrity tweets: {len(df)} loaded.\n{df.head()}')

    df = load_sanders_tweets()
    print(f'Sanders tweets: {len(df)} loaded.\n{df.head()}')

    df = load_cikm_tweets()
    print(f'CIKM tweets: {len(df)} loaded.\n{df.head()}')

if __name__ == '__main__':
    debug()
