import twitter
import json
import dev_login as tc
"""
this module grabs user ids from the most popular/revelant tweets within the past 7 days around the SU/ESF campus
YOU SHOULD IMPORT the file if you wanna use the grab user id function:         gather_user_ids(day-of-month)
"""
twitter_api = tc.oauth_login()

#filter tweets by location: defined as syracuse university 

#also taking into account of the fact that the SU community is diverse and users might tweet with another language. 
def gather_screen_names_covid(day):
    #full version should be: 
        #def gather_user_ids(year, month, day): 
    init_date = 1
    #since we are pass the 7th of may and nowhere close to the last 7 days of may: 
    init_date = day - 7
    users = []
    for i in range(7):
        date = init_date + i 
        temp = "COVID OR pandemic until:2021-05-" + str(date) + " -filter:retweets"
        users.extend(grab_screen_names_day(temp))
    
    screen_names = []
    for i in range(len(users)):
        screen_names.append(users[i]['screen_name'])
        
    return screen_names
    


def grab_screen_names_day(temp):
    
    results = twitter_api.search.tweets(q = temp, lang="en", count=1000, geocode='43.035198,-76.139297,10mi')['statuses']
    users = [r['user'] for r in results]
    return users

print()