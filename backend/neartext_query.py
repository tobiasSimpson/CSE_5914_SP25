import weaviate
import os
import json
import weaviate.classes as wvc
from weaviate.classes.aggregate import GroupByAggregate
from import_data import init_client

wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
openai_api_key = os.environ.get("OPENAI_API_KEY")

def run_sentiment_aggregation(client: weaviate.WeaviateClient,  query: str, collection_name: str= "sentiment140"):
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
            ]
        )

        print(response.total_count)
        print(response.properties)
    except Exception as e:
        print(f"Error during aggregation: {e}")
        return None


def run_neartext(client: weaviate.WeaviateClient, query: str = "social", collection_name: str = "sentiment140"):
    tweets = client.collections.get(name=collection_name)
    # tweets = client.collections.get("sentiment140")
    # print number of items in the collection:
    print(f"Number of items in the collection: {tweets.data.__sizeof__()}")
    response = tweets.query.near_text(
        query=query,
        limit=10
    )

    seen = set()
    for obj in response.objects:
        if obj.properties["text"] in seen:
            continue
        seen.add(obj.properties["text"])
        print(json.dumps(obj.properties, indent=2))


if __name__ == "__main__":
    client = init_client()
    query_text='technology'
    run_neartext(client=client, query='virus', collection_name="sentiment140")
    run_sentiment_aggregation(client=client, query='technology', collection_name="sentiment140")
    client.close()