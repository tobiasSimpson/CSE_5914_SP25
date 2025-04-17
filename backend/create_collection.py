import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure
import os

# Best practice: store your credentials in environment variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
)


def delete_collection(client: weaviate.WeaviateClient, name: str):
    client.collections.delete(name)

def create_collection(client: weaviate.WeaviateClient, name: str, source_property: str):
    client.collections.create(
        name=name,
        vectorizer_config=[
        Configure.NamedVectors.text2vec_openai(
            name=f"{source_property}_vector",
            source_properties=[source_property],
            model='text-embedding-3-small',
            dimensions=512
        )
        ]
    )

# delete_collection(client, "sentiment_tweets")  # Delete if it exists
# delete_collection(client, "Sentiment140")  # Delete if it exists
create_collection(client, "celebrity", "text")  # Create new collection

print(f'current collections are : {[c for c in client.collections.list_all()]}')

# do nothing..

client.close()