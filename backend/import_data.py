import weaviate
from weaviate.classes.init import Auth
import json, os

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
cohere_api_key = os.environ["COHERE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key}
)

# data is of the form [{'tweet':'', 'date':'',...}, {}, ...]
json_list = open("data/data.json", "r").read()
tweet_data = json.loads(json_list)

tweets_collection = client.collections.get("tweets")

with tweets_collection.batch.fixed_size(batch_size=1) as batch:
    for data_row in tweet_data:
        batch.add_object({
            "topic": data_row["topic"],
            "text": data_row["text"],
            "date": data_row["date"],
        })
        if batch.number_errors > 10:
            print("Batch import stopped due to excessive errors.")
            break

failed_objects = tweets_collection.batch.failed_objects
if failed_objects:
    print(f"Number of failed imports: {len(failed_objects)}")
    print(f"First failed object: {failed_objects[0]}")

client.close()