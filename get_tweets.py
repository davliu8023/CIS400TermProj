import twitter
import json

#input dev credentials 
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
    
auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                            CONSUMER_KEY, CONSUMER_SECRET)
    
api = twitter.Twitter(auth=auth)


### UNCOMMENT only one date to get the tweets from the specific date
q= "until:2021-05-11 -filter:retweets" #get twitters from May 10th 
#q= "until:2021-05-10 -filter:retweets" #get twitters from May 9th 
#q= "until:2021-05-9 -filter:retweets" #get twitters from May 8th 
#q= "until:2021-05-8 -filter:retweets" #get twitters from May 7th 
#q= "until:2021-05-7 -filter:retweets" #get twitters from May 6th 
#q= "until:2021-05-6 -filter:retweets" #get twitters from May 5th 
#q= "until:2021-05-5 -filter:retweets" #get twitters from May 4th 
#q= "until:2021-05-4 -filter:retweets" #get twitters from May 3th 

results = api.search.tweets(q=q, lang="en", count=100, geocode='43.035198,-76.139297,10mi')['statuses']
# results uses SU geocode to find tweets within the SU campus
# langauge tag set to english cuz we are not analyzing anything other than english 

tweets = [r['text'] for r in results]

print(tweets)
