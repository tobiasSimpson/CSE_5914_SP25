import weaviate.classes as wvc
from weaviate.classes.init import Auth
from weaviate.classes.aggregate import GroupByAggregate
from import_data import init_client
from openai import OpenAI
from typing import Dict, List, Tuple
import random
import os

client = init_client()

tweets = client.collections.get("sentiment140")
openai_api_key = os.environ.get("OPENAI_API_KEY")

GPT_MODEL_NAME = "gpt-4o-mini"
OAI_CLIENT = OpenAI(api_key=openai_api_key)
MY_USERNAME = "echo_x"


def get_sentiment_aggregation(query:str):
    response = tweets.aggregate.near_text(
        query=query,
        distance=0.8,
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
    if (num_tweets == 0):
        return {
            "positive": 0,
            "negative": 0,
        }
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


def get_one_tweet(query: str):
    response = tweets.query.near_text(
        query=query,
        limit=1,
    )

    # Deduplicate the results
    text = response.objects[0].properties["text"]

    return text

def generate_thread(
    seed_user_tweet: str,
    grouped_tweets: Dict[str, List[str]],
    style: str,
    num_tweets_in_thread: int = 5,
):
    """
    Generate a thread of tweets based on the seed tweet and celebrity tweets.
    """
    num_tweets_per_celeb = {
        celeb: len(tweets) for celeb, tweets in grouped_tweets.items()
    }
    celeb_list = [celeb for celeb, count in num_tweets_per_celeb.items()]
    celeb_probabilities = [
        count / sum(num_tweets_per_celeb.values())
        for count in num_tweets_per_celeb.values()
    ]
    # print(f"seed tweet: {seed_user_tweet}")
    # print(f"celebrity counts: {num_tweets_per_celeb}")
    # print(f"Celebrity probabilities: {celeb_probabilities}")
    current_thread = [(MY_USERNAME, seed_user_tweet)]
    for _ in range(num_tweets_in_thread):
        # choose celeb based on probabilities, reweight to make them less likely next:
        celeb = random.choices(celeb_list, weights=celeb_probabilities, k=1)[0]
        celeb_probabilities[celeb_list.index(celeb)] *= 0.6
        celeb_probabilities = [
            count / sum(celeb_probabilities) for count in celeb_probabilities
        ]
        # print(f"Chosen celeb: {celeb}")
        next_tweet = continue_thread(current_thread, celeb, grouped_tweets[celeb], style)
        current_thread.append((celeb, next_tweet))
        # break
    
    # print('Final thread:', "\n".join(current_thread))

    list_of_tweets = [obj[0] + ": " + obj[1] for obj in current_thread]
    return list_of_tweets

    return current_thread

def continue_thread(
    current_thread: List[Tuple[str, str]],
    celeb: str,
    celeb_tweets: List[str],
    style: str,
) -> str:
    """
    Call the LLM to continue the Twitter thread. Returns the generated tweet text.
    Appends the new tweet (by celeb) to current_thread.
    """
    # Build the “thread so far” context
    thread_context = "\n".join(f"{author}: {text}" for author, text in current_thread[-3:])

    # Build a short style reference from the celeb's past tweets
    style_reference = "\n".join(f"- {t}" for t in celeb_tweets[:6])

    user_tweets = [t for t in current_thread if t[0] == MY_USERNAME]
    starter = user_tweets[-1][1] if user_tweets else current_thread[0][1]
    # Assemble a single-user prompt
    user_msg = {
        "role": "user",
        "content": (
            "You are a social-media copywriter. "
            f"You're going to write a Twitter reply as {celeb}, "
            f"continuing an existing thread in a {style} style."
            "Here’s the thread so far:\n"
            f"{thread_context}\n\n"
            f'Original tweet conversation starter: "{starter}"\n\n'
            f"Style reference (past {celeb} tweets):\n"
            f"{style_reference}\n\n"
            "Write the *next* concise tweet (≤180 chars) from "
            f"{celeb} that sticks closely to {celeb}'s previous tweets but follows a {style} style.\n"
        ),
    }

    resp = OAI_CLIENT.chat.completions.create(
        model=GPT_MODEL_NAME,
        messages=[user_msg],
        max_tokens=160,
        temperature=0.4,
        n=1,
    )
    tweet = resp.choices[0].message.content.strip().strip('"')
    # print(f"[{celeb}] {tweet}")
    return tweet


def run_groupby_neartext(
    query: str,
    groupby_val: str,
    collection_name: str = "celebrity",
):
    tweets = client.collections.get(name=collection_name)

    # response = tweets.query.near_text(
    #     query=query,
    #     limit=10,
    #     group_by=["username"],
    # )
    # response = tweets.aggregate.near_text(
    #     group_by=GroupByAggregate(prop="username"),
    #     query=query,
    #     object_limit=200
    # )

    response = tweets.query.near_text(
        query=query,
        limit=100,
    )

    seen = set()
    celeb_tweets = []
    for obj in response.objects:
        if obj.properties["text"] in seen or len(obj.properties["text"]) < 20:
            continue
        seen.add(obj.properties["text"])
        celeb_tweets.append(obj.properties)
        # print(json.dumps(obj.properties, indent=2))

    featured_celebs = {obj["username"] for obj in celeb_tweets}
    print(f"Featured celebs: {featured_celebs}")
    grouped_tweets = {celeb: [] for celeb in featured_celebs}
    for celeb in featured_celebs:
        grouped_tweets[celeb] = [
            obj["text"].replace("\\n", "")
            for obj in celeb_tweets
            if obj["username"] == celeb
        ]

    return grouped_tweets


def make_request(query: str):
    # Make both requests and return the results
    sentiment = get_sentiment_aggregation(query)
    # tweets = get_neartext(query)
    single_tweet = get_one_tweet(query)
    celeb_tweets = run_groupby_neartext(
        query=single_tweet,
        groupby_val="username",
        collection_name="celebrity",
    )
    thread = generate_thread(single_tweet, celeb_tweets, "argumentative")

    return {
        "sentiment": sentiment,
        "tweets": thread
    }

def close():
    client.close()
