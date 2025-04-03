# Import all the stuff





df=[]

def get_sentiment(topic):
    sentiment = {"positive": 0, "negative": 0}
    for tweet in df:
        if (topic.lower() in tweet.text.lower()):
            if (tweet.sentiment == 4):
                sentiment["positive"] += 1
            elif (tweet.sentiment == 0):
                sentiment["negative"] += 1
    return sentiment