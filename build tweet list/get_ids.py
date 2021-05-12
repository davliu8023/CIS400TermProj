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
#q= "until:2021-05-11 -filter:retweets" #get twitters from May 10th 
#q= "until:2021-05-10 -filter:retweets" #get twitters from May 9th 
#q= "until:2021-05-9 -filter:retweets" #get twitters from May 8th 
#q= "until:2021-05-8 -filter:retweets" #get twitters from May 7th 
#q= "until:2021-05-7 -filter:retweets" #get twitters from May 6th 
#q= "until:2021-05-6 -filter:retweets" #get twitters from May 5th 
#q= "until:2021-05-5 -filter:retweets" #get twitters from May 4th 
#q= "until:2021-05-4 -filter:retweets" #get twitters from May 3th 
def gather_user_ids(day):#input should be yearmonthdate example 2021 Jan 21st should be gather_user_id(21) 
    #full version should be: 
        #def gather_user_ids(year, month, day): 
    init_date = 1
    ''' THE following commented out codes are for general purposes to handle exceptions and different lengths of months 
    within the year but not necessary for our purposes so I did not finish this part of the code
    if (year != 2021 or month <= 0 or month >= 13 or day <= 0 or day >= 31):
        print("Wrong input!")
        return 
    if (day >= 7 and day <= 30):
        init_date = day - 7
    elif (day < 7):
        temp = 7 - day 
        if (month in (1, 3, 5, 7, 8, 10, 12)):
            init_date = 31 - temp 
        elif (month == 2): 
            init_date = 
    '''
    #since we are pass the 7th of may and nowhere close to the last 7 days of may: 
    init_date = day - 7
    ids = []
    for i in range(7):
        date = init_date + i 
        temp = "until:2021-05-" + str(date) + " -filter:retweets"
        ids.extend(gather_user_ids_day(temp))
    #print (list(set(ids)))
    return (list(set(ids)))
    


def gather_user_ids_day(temp):
    
    results = twitter_api.search.tweets(q = temp, lang="en", count=1000, geocode='43.035198,-76.139297,10mi')['statuses']
    ids = [r['id'] for r in results]
    return ids

#gather_user_ids(12)