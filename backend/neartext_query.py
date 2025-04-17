from typing import Dict, List, Tuple
import weaviate
import os
import json
import random
from openai import OpenAI

import weaviate.classes as wvc
from import_data import init_client
from weaviate.classes.aggregate import GroupByAggregate
from weaviate.classes.query import GroupBy


wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
openai_api_key = os.environ.get("OPENAI_API_KEY")

GPT_MODEL_NAME = "gpt-4o-mini"
OAI_CLIENT = OpenAI(api_key=openai_api_key)
MY_USERNAME = "echo_x"

def run_sentiment_aggregation(
    client: weaviate.WeaviateClient, query: str, collection_name: str = "sentiment140"
):
    try:
        collection = client.collections.get(collection_name)
        response = collection.aggregate.near_text(
            query=query,
            distance=0.9,
            object_limit=200,
            total_count=True,
            return_metrics=[
                wvc.query.Metrics("sentiment").integer(
                    count=True,
                    maximum=True,
                    mean=True,
                    median=True,
                    minimum=True,
                    mode=True,
                    sum_=True,
                ),
            ],
        )

        print("Total count of tweets aggregated:", response.total_count)
        print("Aggregated results:")
        print(response.properties)

    finally:
        client.close()


def run_neartext(
    client: weaviate.WeaviateClient, query: str, collection_name: str = "sentiment140"
):
    tweets = client.collections.get(name=collection_name)
    # tweets = client.collections.get("sentiment140")
    # print number of items in the collection:
    print(f"Number of items in the collection: {tweets.data.__sizeof__()}")
    response = tweets.query.near_text(query=query, limit=10)

    seen = set()
    for obj in response.objects:
        if obj.properties["text"] in seen:
            continue
        seen.add(obj.properties["text"])
        print(json.dumps(obj.properties, indent=2))


def run_groupby_neartext(
    client: weaviate.WeaviateClient,
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
        limit=150,
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

def display_tweet(tweet: Tuple[str, str], accept_input: bool = False) -> str:
    user, text = tweet
    # display in a neat format inside a box with a border:
    print(f"\n{'_' * 60}\n")
    if accept_input:
        text = input(f"@{MY_USERNAME}\n\t")
    else:
        print(f"@{user}\n", end='')
        # print text with max width of 50, wrap otherwise.
        # do not cut off words.
        parts = text.split()
        tot='\t'
        for part in parts:
            if len(tot) + len(part) > 45:
                print(tot)
                tot = '\t'
            tot+=part+' '
        print(tot)
    print(f"{'_' * 60}",end='')
    
    return text

def generate_thread(
    seed_user_tweet: str,
    grouped_tweets: Dict[str, List[str]],
    style: str,
    num_tweets_in_thread: int = 8,
    allow_interruption:bool = False,
    do_display:bool = True,
):
    """
    Generate a thread of tweets based on the seed tweet and celebrity tweets.
    """
    # possible_groups = ['BarackObama', 'realDonaldTrump', 'KimKardashian', 'BillGates', 'Oprah', 'justinbieber', 'TheRock', 'elonmusk', 'JeffBezos', 'katyperry']
    # Generate a thread of tweets based on the seed tweet and celebrity tweets.
    # print(f"Generating thread for seed tweet: {seed_user_tweet}")
    # print(f"Style: {style}")
    # print(f"Celebrity tweets: {grouped_tweets}")
    num_tweets_per_celeb = {
        celeb: len(tweets) for celeb, tweets in grouped_tweets.items()
    }
    celeb_list = [celeb for celeb, count in num_tweets_per_celeb.items()]
    if 'realDonaldTrump' in celeb_list:
        num_tweets_per_celeb['realDonaldTrump'] = 80
    celeb_probabilities = [
        count / sum(num_tweets_per_celeb.values())
        for count in num_tweets_per_celeb.values()
    ]
    # print(f"seed tweet: {seed_user_tweet}")
    # print(f"celebrity counts: {num_tweets_per_celeb}")
    # print(f"Celebrity probabilities: {celeb_probabilities}")
    current_thread = [(MY_USERNAME, seed_user_tweet)]
    if do_display:
        display_tweet(current_thread[0])
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
        if do_display:
            display_tweet(current_thread[-1])
        if allow_interruption and random.random() < 0.4:
            # get tweet from user:
            if do_display:
                user_tweet = display_tweet(current_thread[-1], accept_input=True)
            current_thread.append((MY_USERNAME, user_tweet))
        # break
    
    # print('Final thread:', "\n".join(current_thread))
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


if __name__ == "__main__":
    client = init_client()
    seed_tweet = "sometimes college classes can be difficult"

    # print(f'{"*"*12} Running neartext query for "{query_text}": {"*"*12}')
    # run_neartext(client=client, query=query_text, collection_name="sentiment140")

    # print(f'\n{"*"*12} Running sentiment aggregation for "{query_text}": {"*"*12}')
    # run_sentiment_aggregation(client=client, query=query_text, collection_name="sentiment140")
    
    style = "argumentative"
    celeb_tweets = run_groupby_neartext(
        client=client,
        query=seed_tweet,
        groupby_val="username",
        collection_name="celebrity",
    )
    
    ai_tweets = generate_thread(seed_tweet, celeb_tweets, style, allow_interruption=False, do_display=False)
    print(ai_tweets)

    client.close()
