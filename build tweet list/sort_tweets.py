
import functools
import twitter
import time
import json
import sys
import urllib.request
import urllib.error

#Keys, authorization and twitter initialization
#Added parameter so my function would automatically sleep on rate limits,
#instead of crashing and forcing me to start over
#I tried to minimize calls, but you may encounter this
CONSUMER_KEY = 'McRM2Poc1GfpGmzC3V704PFqx'
CONSUMER_SECRET = '3chcGmJsS2WLRef3tbN0b4vNLoEQSljcHvnR3ERBby2CPseKrJ'
OAUTH_TOKEN = '1369344805122277384-GNw1gd06Knf0jxqpDhcomzf3IdrNRs'
OAUTH_TOKEN_SECRET = '6HrghNeiREUbebYP0euvQxV3tLf6AlF6dIE1wgNq4SB43'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
CONSUMER_KEY, CONSUMER_SECRET)
twitter_api = twitter.Twitter(auth=auth)

#make_twitter_request is required for get_friends_followers_ids to work, so I
#copied it (and its associated comments) from the Twitter Cookbook,
#with some modifications to make it run on Python 3.
#I later realized it could be useful in my own code and added it there as well
#(I have indicated in the comments when that happens.)
def make_twitter_request(twitterFunction, max_errors=3, *args, **kwArgs): 

    # A nested function for handling common HTTPErrors. Return an updated value 
    # for wait_period if the problem is a 503 error. Block until the rate limit is 
    # reset if a rate limiting issue

    def handle_http_error(e, wait_period=2):

        if wait_period > 3600: # Seconds
            print('Too many retries. Quitting.')
            raise e

        if e.e.code == 401:
            print('Encountered 401 Error (Not Authorized)')
            return None

        if e.e.code in (502, 503):
            print('Encountered %i Error. Will retry in %i seconds' % \
                    (e.e.code, wait_period))
            time.sleep(wait_period)
            wait_period *= 1.5
            return wait_period

        # Rate limit exceeded. Wait 15 mins. See https://dev.twitter.com/docs/rate-limiting/1.1/limits
        if e.e.code == 429: 
            now = time.time()  # UTC
            sleep_time = 15*60 # 15 mins
            print('Rate limit reached: sleeping for 15 mins')
            time.sleep(sleep_time)
            return 0

        # What else can you do?
        raise e

    wait_period = 2
    error_count = 0
    while True:
        try:
            return twitterFunction(*args, **kwArgs)
        except twitter.api.TwitterHTTPError as e:
            error_count = 0
            wait_period = handle_http_error(e, wait_period)
            if wait_period is None:
                return
        except URLError as e:
            error_count += 1
            print("URLError encountered. Continuing.")
            if error_count > max_errors:
                print("Too many consecutive errors...bailing out.")
                raise

def harvest_user_timeline(twitter_api, screen_name=None, user_id=None, max_results=1000):
     
    assert (screen_name != None) != (user_id != None), \
    "Must have screen_name or user_id, but not both"    
    
    kw = {  # Keyword args for the Twitter API call
        'count': 200,
        'trim_user': 'true',
        'include_rts' : 'true',
        'since_id' : 1
        }
    
    if screen_name:
        kw['screen_name'] = screen_name
    else:
        kw['user_id'] = user_id
        
    max_pages = 16
    results = []
    
    tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
    
    if tweets is None: # 401 (Not Authorized) - Need to bail out on loop entry
        tweets = []
        
    results += tweets
    
    print >> sys.stderr, 'Fetched %i tweets' % len(tweets)
    
    page_num = 1
    
    # Many Twitter accounts have fewer than 200 tweets so you don't want to enter
    # the loop and waste a precious request if max_results = 200.
    
    # Note: Analogous optimizations could be applied inside the loop to try and 
    # save requests. e.g. Don't make a third request if you have 287 tweets out of 
    # a possible 400 tweets after your second request. Twitter does do some 
    # post-filtering on censored and deleted tweets out of batches of 'count', though,
    # so you can't strictly check for the number of results being 200. You might get
    # back 198, for example, and still have many more tweets to go. If you have the
    # total number of tweets for an account (by GET /users/lookup/), then you could 
    # simply use this value as a guide.
    
    if max_results == kw['count']:
        page_num = max_pages # Prevent loop entry
    
    while page_num < max_pages and len(tweets) > 0 and len(results) < max_results:
    
        # Necessary for traversing the timeline in Twitter's v1.1 API:
        # get the next query's max-id parameter to pass in.
        # See https://dev.twitter.com/docs/working-with-timelines.
        kw['max_id'] = min([ tweet['id'] for tweet in tweets]) - 1 
    
        tweets = make_twitter_request(twitter_api.statuses.user_timeline, **kw)
        results += tweets

        print >> sys.stderr, 'Fetched %i tweets' % (len(tweets),)
    
        page_num += 1
        
    print >> sys.stderr, 'Done fetching tweets'

    return results[:max_results]

tweetlist = []
for user in userids
    tweetadd = harvest_user_timeline(twitter_api, user_id = user)
    for tweet in tweetadd
        tweetlist.append(tweet)

covidtweetlist = [twt for twt in tweetlist if "covid" in twt['text']
                  or "mask" in twt['text'] or "online" in twt['text']
                  or "six feet" in twt['text'] or "6 feet" in twt['text']
                  or "social distancing" in twt['text']

vaccinetweetlist = [twt for twt in tweetlist if "vaccine" in twt['text']
                    or "pfizer" in twt['text'] or "johnson" in twt['text']
                    or "moderna" in twt['text'] or "shot" in twt['text']]


