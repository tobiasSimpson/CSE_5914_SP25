import weaviate
from weaviate.classes.init import Auth
import os, json

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
cohere_api_key = os.environ["COHERE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key},
)

tweets = client.collections.get("tweets")

response = tweets.query.near_text(
    query="technology",
    limit=5
)

for obj in response.objects:
    print(json.dumps(obj.properties, indent=2))

client.close()  # Free up resources