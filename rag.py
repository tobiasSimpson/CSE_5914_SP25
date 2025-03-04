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

# get topic query from the user:
query = input('Enter a query for tweet RAG: ')

response = questions.generate.near_text(
    query=query,
    limit=10,   # can't be too high
    grouped_task="Create a concise twitter-style post including the information in the following tweets. Do NOT include any extraneous text, ONLY directly generate the resulting tweet.",
)

print(f'QUERY: "{query}"\n')

seen_text = set()
for obj in response.objects:
    text = obj.properties['text']
    if text in seen_text:
        continue
    seen_text.add(text)
    if len(text) <20:
        continue
    print('💬 '+obj.properties['text'])

generated_text = response.generated.strip('"')

print(f'\n🤖 {response.generated}')

client.close()
