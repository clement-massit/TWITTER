import json

path = 'C:\\wamp64\\www\\TWITTER\\tweets json format\\tweets.json'
with open(path, 'r') as tweet_file:
    data = json.load(tweet_file)
    print(data['created_at'])
        

