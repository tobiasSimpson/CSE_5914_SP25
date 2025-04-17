import json
import os
import time
from datetime import datetime

import weaviate
from tqdm import tqdm
from weaviate.classes.init import Auth
from typing import List

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
openai_api_key = os.environ["OPENAI_API_KEY"]

def add_data(client: weaviate.WeaviateClient, collection_name: str, data: List[dict]) -> None:
    """
    {
        "sentiment": data_row["target"],
        "username": data_row["user"],
        "text": data_row["text"],
        "date": data_row["date"],
    }
    """

    collection = client.collections.get(collection_name)

    with collection.batch.dynamic() as batch:
        for src_obj in tqdm(data):
            batch.add_object(
                properties={
                    # "sentiment": src_obj["target"],
                    "username": src_obj["username"],
                    "text": src_obj["text"],
                    # "date": src_obj["date"],
                },
            )
            if batch.number_errors > 10:
                print("Batch import stopped due to excessive errors.")
                break
    failed_objects = collection.batch.failed_objects
    if failed_objects:
        print(f"Number of failed imports: {len(failed_objects)}")
        print(f"First failed object: {failed_objects[0]}")


def init_client() -> weaviate.WeaviateClient:
    """
    Initialize the Weaviate client.
    """
    headers = {
        "X-OpenAI-Api-Key": openai_api_key,
    }
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=wcd_url,
        auth_credentials=Auth.api_key(wcd_api_key),
        headers=headers,
    )
    return client


def main():
    client = init_client()
    file = open("data/celebrity_tweets.json", "r")
    # file = open("data/sentiment_140.json", "r")
    json_list = file.read()
    data = json.loads(json_list)
    
    # sort data in ascending order of 'sentiment' value:
    # data.sort(key=lambda x: x['target'], reverse=True)  # sort by sentiment value
    data_collection = client.collections.get("celebrity")

    # TOTAL_N_ITEMS = 10000
    TOTAL_N_ITEMS = len(data)
    data = data[:TOTAL_N_ITEMS] if TOTAL_N_ITEMS > 0 else data
    print(f'adding {len(data)} new items to the collection...')
    add_data(client, "celebrity", data)
    file.close()
    client.close()

if __name__ == "__main__":
    # main()
    print('Done!')