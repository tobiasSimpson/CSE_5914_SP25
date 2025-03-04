import weaviate
from weaviate.classes.init import Auth
import os

wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
)

print(client.is_ready())
client.close()
# should print `True`

"""
export WCD_URL="https://vivw2msbwnqtysrotsqa.c0.us-east1.gcp.weaviate.cloud"
export WCD_API_KEY="9rdQkROFdIPKvxH7GcCDlNLGNRWOw4Gr66j7"
export COHERE_API_KEY=466SIWQwWoiLeyot0wfIHdqavbYIZfwPTkiblXuY
"""