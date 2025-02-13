import weaviate
from weaviate.classes.init import Auth
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

query = 'technology, phones'
response = questions.generate.near_text(
    query=query,
    limit=10,
    grouped_task="Create a concise twitter-style post assimilating the information in the following tweets. Do not include any extraneous text, directly generate the resulting tweet.",
)

print(f'QUERY: "{query}"\n')

for obj in response.objects:
    text = obj.properties['text']
    if len(text) <20:
        continue
    print('💬 '+obj.properties['text'])

print(f'\n🤖 {response.generated}')

client.close()
