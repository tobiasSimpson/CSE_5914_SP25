import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.aggregate import GroupByAggregate
import os

wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
cohere_api_key = os.environ["COHERE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
    headers={"X-Cohere-Api-Key": cohere_api_key}
)

questions = client.collections.get("tweets")

def make_request(query):
    response = questions.generate.near_text(
        query=query,
        limit=10,   # can't be too high
        grouped_task="Create a concise twitter-style post including the information in the following tweets. Do NOT include any extraneous text, ONLY directly generate the resulting tweet.",
    )

    text = {obj.properties["text"] for obj in response.objects}
    generated_text = response.generated.strip('"')
    return {'text': list(text), 'generated': generated_text}


def close():
    client.close()
