import twitter 
import dev_login as api 
import fetch_screen_names as screenName
import sort_tweets as st
import re, string, random
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
#import sort_tweets as st

def remove_noise(tweet, stop_words = ()):
    clean_tweet = []
    for token, tag in pos_tag(tweet):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            clean_tweet.append(token.lower())
    return clean_tweet

def get_all_words(clean_tweet_list):
    for tokens in clean_tweet_list:
        for token in tokens:
            yield token

def get_tweets_for_model(clean_tweet_list):
    for tweet in clean_tweet_list:
        yield dict([token, True] for token in tweet)

if __name__ == "__main__": 
    twitter_api = api.oauth_login()
    tweetlist = []
    tweetlist_covid = []
    tweetlist_vaccine = []

    screennames = screenName.gather_screen_names(12)
    #tweetlist_covid = []
    #screennames_covid = screenName.gather_screen_names_covid(12)
    ##for i in range(100): 
    #    temp_list.append(screennames[i])
    temp_list = screennames #NOTE that right here we are going all out with all user screen names 
    #but for laptops/computers with lesser amount of ram/swap, you might have to have a smaller sample size 
            #for each run 

    progress = 0
    for user in temp_list: 
        progress += 1
        print("Fetching " + user +"'s Tweets")
        tweetadd = st.harvest_user_timeline(twitter_api, screen_name=user, max_results= 100 )
        print("Progress "+ str(progress)+ " out of "+(str(len(temp_list)))+" defined users loaded")
        for i in tweetadd: 
            tweetlist.append(i['text'])

    for tweet in tweetlist: 
        if ("covid" in tweet or "mask" in tweet or "online" in tweet or "six feet" in tweet or "6 feet" in tweet or "social distancing" in tweet): 
            tweetlist_covid.append(tweet)
        if ("vaccine" in tweet or "pfizer" in tweet or "johnson" in tweet or "moderna" in tweet or "shot" in tweet):
            tweetlist_vaccine.append(tweet)
        
    positive_tweets = twitter_samples.strings('positive_tweets.json')
    negative_tweets = twitter_samples.strings('negative_tweets.json')
    text = twitter_samples.strings('tweets.20150430-223406.json')
    tweet = twitter_samples.tokenized('positive_tweets.json')[0]
    stop_words = stopwords.words('english')
    positive_tweet = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet = twitter_samples.tokenized('negative_tweets.json')
    positive_clean_tweet_list = []
    negative_clean_tweet_list = []
    for tokens in positive_tweet:
        positive_clean_tweet_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet:
        negative_clean_tweet_list.append(remove_noise(tokens, stop_words))
    all_pos_words = get_all_words(positive_clean_tweet_list)
    freq_dist_pos = FreqDist(all_pos_words)
    #print(freq_dist_pos.most_common(10))
    positive_tokens_for_model = get_tweets_for_model(positive_clean_tweet_list)
    negative_tokens_for_model = get_tweets_for_model(negative_clean_tweet_list)
    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]
    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]
    dataset = positive_dataset + negative_dataset
    random.shuffle(dataset)
    train_data = dataset[:7000]
    test_data = dataset[7000:]
    classifier = NaiveBayesClassifier.train(train_data)
    print("Accuracy is:", classify.accuracy(classifier, test_data))
    #print(classifier.show_most_informative_features(10))
    #print(custom_tweet, classifier.classify(dict([token, True] for token in custom_tokens)))

    if (len(tweetlist_covid) > 0): 
        pos_cntc = 0
        neg_cntc = 0 
        neutral_cntc = 0
        total_cntc = 0
        sentimentsc = []
        for tweets in tweetlist_covid: 
            custom_tokens = remove_noise(word_tokenize(tweets))
            sample_sentiment = classifier.classify(dict([token, True] for token in custom_tokens))
            sentimentsc.append(sample_sentiment)
            if (sample_sentiment == "Positive"): 
                pos_cntc += 1
            elif (sample_sentiment == "Negative"): 
                neg_cntc += 1
            else: 
                neutral_cntc += 1
        print("COVID Positive Sentiment Count: " + str(pos_cntc))
        print("COVID Negative Sentiment Count: " + str(neg_cntc))
        print("COVID Neutral Sentiment: " + str(neutral_cntc))
        if (pos_cntc > neg_cntc): 
            print("Overall, COVID tweets are positive with a percentage of " + str("{:.2f}".format(((pos_cntc - neg_cntc)/neg_cntc)*100)) + "% of more tweets that are positive")
        elif (neg_cntc > pos_cntc): 
            print("Overall, COVID tweets are negative with a percentage of " + str("{:.2f}".format(((neg_cntc - pos_cntc)/pos_cntc)*100)) + "% of more tweets that are negative")

    if (len(tweetlist_vaccine) > 0): 
        pos_cntc = 0
        neg_cntc = 0 
        neutral_cntc = 0
        total_cntc = 0
        sentimentsc = []
        for tweets in tweetlist_vaccine: 
            custom_tokens = remove_noise(word_tokenize(tweets))
            sample_sentiment = classifier.classify(dict([token, True] for token in custom_tokens))
            sentimentsc.append(sample_sentiment)
            if (sample_sentiment == "Positive"): 
                pos_cntc += 1
            elif (sample_sentiment == "Negative"): 
                neg_cntc += 1
            else: 
                neutral_cntc += 1
        print("VACCINE Positive Sentiment Count: " + str(pos_cntc))
        print("VACCINE Negative Sentiment Count: " + str(neg_cntc))
        print("VACCINE Neutral Sentiment: " + str(neutral_cntc))
        if (pos_cntc > neg_cntc): 
            print("Overall, VACCINE tweets are positive with a percentage of " + str("{:.2f}".format(((pos_cntc - neg_cntc)/neg_cntc)*100)) + "% of more tweets that are positive")
        elif (neg_cntc > pos_cntc): 
            print("Overall, VACCINE tweets are negative with a percentage of " + str("{:.2f}".format(((neg_cntc - pos_cntc)/pos_cntc)*100)) + "% of more tweets that are negative")


    pos_cnt = 0
    neg_cnt = 0 
    neutral_cnt = 0
    total_cnt = 0
    sentiments = []
    for tweets in tweetlist: 
        custom_tokens = remove_noise(word_tokenize(tweets))
        sample_sentiment = classifier.classify(dict([token, True] for token in custom_tokens))
        sentiments.append(sample_sentiment)
        if (sample_sentiment == "Positive"): 
            pos_cnt += 1
        elif (sample_sentiment == "Negative"): 
            neg_cnt += 1
        else: 
            neutral_cnt += 1

    print("Out of " + str(len(tweetlist)) + " tweets colleted from " + str(len(screennames)) + " twitter users within the SU community: ")
    print("General Positive Sentiment Count: " + str(pos_cnt))
    print("General Negative Sentiment Count: " + str(neg_cnt))
    print("General Neutral Sentiment: " + str(neutral_cnt))


        

    if (pos_cnt > neg_cnt): 
        print("Overall, general tweets are positive with a percentage of " + str("{:.2f}".format(((pos_cnt - neg_cnt)/neg_cnt)*100)) + "% of more tweets that are positive")
    elif (neg_cnt > pos_cnt): 
        print("Overall, general tweets are negative with a percentage of " + str("{:.2f}".format(((neg_cnt - pos_cnt)/pos_cnt)*100)) + "% of more tweets that are negative")




    

    '''
for user in userids:
    tweetadd = harvest_user_timeline(twitter_api, user_id = user)
    for tweet in tweetadd:
        tweetlist.extend(tweet)

covidtweetlist = [twt for twt in tweetlist if "covid" in tweet
                  or "mask" in tweet or "online" in tweet
                  or "six feet" in tweet or "6 feet" in tweet
                  or "social distancing" in tweet]

vaccinetweetlist = [twt for twt in tweetlist if "vaccine" in tweet
                    or "pfizer" in tweet or "johnson" in tweet
                    or "moderna" in tweet or "shot" in tweet]


'''



