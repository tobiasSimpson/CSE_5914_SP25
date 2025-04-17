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
2. Make sure you have docker installed
3. Export your Weaviate Cloud Database (WCD) URL, the WCD API key and the OpenAI API key as environment variables as `WCD_URL, WCD_API_KEY, OPENAI_API_KEY` respectively.  Put these in a file called `backend.env` in this directory.  The file should look like the following:
```dotenv
WCD_URL="https://something.weaviate.cloud"
WCD_API_KEY="something"
OPENAI_API_KEY="something"
```

4. `docker compose up` will start the application at http://localhost.  You may need to use sudo to run this, and you can add `-d` to run in detached mode.
