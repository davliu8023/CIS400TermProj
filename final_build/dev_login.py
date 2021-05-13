"""
This file handles dev login 
please copy paste your dev credentials 
"""
import twitter 

def oauth_login():
    # XXX: Go to http://twitter.com/apps/new to create an app and get values
    # for these credentials that you'll need to provide in place of these
    # empty string values that are defined as placeholders.
    # See https://developer.twitter.com/en/docs/basics/authentication/overview/oauth
    # for more information on Twitter's OAuth implementation.
    
    CONSUMER_KEY = 'W64i02NmzrI3kTRRPIVdV8toJ'
    CONSUMER_SECRET = 'lFfnnz9oEnS1tUVo5WnsWliFnXWWvYe591VFMR7ad0CUrCrZPW'
    OAUTH_TOKEN = '1375881915643887618-n8fO2YPeJtl94c4SW8NMOQAHOPPbOb'
    OAUTH_TOKEN_SECRET = 'T5koRLTsCvE969erfRzmagLmu2hOYR4ky1sCvVmycgPAW'
    
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)
    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

