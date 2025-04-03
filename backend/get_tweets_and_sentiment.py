import weaviate.classes as wvc
from weaviate.classes.init import Auth
from weaviate.classes.aggregate import GroupByAggregate
from import_data import init_client

client = init_client()

tweets = client.collections.get("sentiment140")


def get_sentiment_aggregation(query:str):
    response = tweets.aggregate.near_text(
        query=query,
        distance=0.9,
        object_limit=200,
        total_count=True,
        return_metrics=[
            wvc.query.Metrics("sentiment").integer(
                sum_=True,
            ),
        ]
    )

    # Positive sentiment has a value 4, and negative sentiment has a value 0
    num_tweets = response.total_count
    total_sentiment = int(response.properties["sentiment"].sum_)
    num_positive = total_sentiment // 4
    num_negative = num_tweets - num_positive
    return {
        "positive": num_positive,
        "negative": num_negative,
    }


def get_neartext(query: str):
    response = tweets.query.near_text(
        query=query,
        limit=10,
        # grouped_task="Create a concise twitter-style post including the information in the following tweets. Do NOT include any extraneous text, ONLY directly generate the resulting tweet.",
    )

    # Deduplicate the results
    text = {obj.properties["text"] for obj in response.objects}

    # generated_text = response.generated.strip('"')
    generated_text = "Fake generated text"
    
    return {'text': list(text), 'generated': generated_text}


def make_request(query: str):
    # Make both requests and return the results
    sentiment = get_sentiment_aggregation(query)
    tweets = get_neartext(query)
    return {
        "sentiment": sentiment,
        "tweets": tweets
    }

def close():
    client.close()
