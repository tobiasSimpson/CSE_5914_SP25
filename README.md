# CSE_5914_SP25

This project aims to develop a Retrieval-Augmented Generation (RAG) system that leverages ElasticSearch for efficiently querying a large database of Tweets and Reddit comments (datasets linked below). 
- Dynamic generation of relevant posts, comments, or threads in response to user-defined topics. 

- ElasticSearch – rapid retrieval of contextual and semantically aligned data from the social media corpus. 

- Data serves as a real-world basis for prompts or supporting material for the generative model. 

- Automated engagement = endorphins go brr.

# Running:
1. Clone this repo:
```
git clone https://github.com/tobiasSimpson/CSE_5914_SP25
```
2. Install `conda` if you haven't already from the [installation page](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html).
3. Create a new `conda` environment and install requirements:
```
conda create --name autoac --file requirements.txt
```
4. Export your Weaviate Cloud Database (WCD) URL, the WCD API key and the Cohere API key as environment variables as `WCD_URL, WCD_API_KEY, COHERE_API_KEY` respectively.

5. `python3 rag.py` will run RAG on your data!
