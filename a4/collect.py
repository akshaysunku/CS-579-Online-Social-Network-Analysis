"""
Collect data.
"""
from TwitterAPI import TwitterAPI
from collections import defaultdict
import pickle
import sys
import time
import csv
import re


consumer_key = 'OGUwQXPBCcP8HxORUBhfISgrf'
consumer_secret = 'FrZZ7BUG1g37WrLpROXrdLCHXV4V4EbdICiEX15k9hWw5rhvDK'
access_token = '2174502762-6LCyy8qbfoaiR2D7CmzgReAkqrUfgqtoMIHmVIB'
access_token_secret = '3Hz7KQmyHYwRypaheLVcboxwqLv85aOrfmiTGxhhLQ9Qc'


def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)



def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        elif request.status_code == 401:
            continue
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)



def get_friends(twitter, userid):
    """ Return a list of Twitter ID's of the friends of the person identified by the 
    userid. We retrieve a maximum of 200 friends.
    Args:
      twitter.... A TwitterAPI object.
      userid..... user_id of the person whose friends IDs are to be fetched.
    Returns:
      A sorted list of friends IDs
    """
    response = robust_request(twitter, 'friends/ids', {'user_id':userid, 'count':200})
    response = [i for i in response]
    if len(response) > 0:
        return sorted(response)
    else:
        return []



def find_friends(twitter, screen_name):
    """ Creates a dictionary of a user to the list of friend IDs of the user
    and write the data to a pickle file.
    Args:
      twitter....... A TwitterAPI object.
      screen_name... screen_name of the user whose friends we want
    Returns:
      Nothing 
    """
    friends_list = defaultdict(list)
    friend = robust_request(twitter, 'friends/ids', {'screen_name':screen_name, 'count':20})
    friend = [i for i in friend]
    friends_list[screen_name] = sorted(friend)

    sorted_friends = sorted(friend)[:20]
    for i in sorted_friends:
        ids = get_friends(twitter, i)
        friends_list[i] = ids

    print("Writing the data to pickle file")
    pickle.dump(friends_list, open('./Collect Data/friends.pkl', 'wb'))



def get_tweets(twitter, topic):
    """ Collect the tweets using the TwitterAPI that contain the given topic.
    Args:
      twitter.... A TwitterAPI object.
      topic...... the topic we want to search the tweets with.
    Returns:
      Nothing
    """
    tweets = robust_request(twitter, 'search/tweets', {'q': topic, 'count':250, 'lang': 'en'})
    tweets = [i for i in tweets]
    write_tweets(tweets)



def write_tweets(tweets):
    """ writes the tweets to a csv file
    Args:
      tweets.... A list of tweets to be written to the csv file
    Returns:
      Nothing
    """
    tweet_count = 0
    file = open('./Collect Data/tweets.csv', 'a')
    csvwriter = csv.writer(file, lineterminator = '\n')
    for tweet in tweets:
        cleaned_tweet = clean_tweet(tweet['text'])
        link = "https://twitter.com/i/web/status/" + str(tweet['id'])  
        tweet_count += 1
        csvwriter.writerow([cleaned_tweet.encode("utf-8"), link])

    file = open('./Collect Data/collect_summary.txt', 'a')
    file.write("Number of tweets collected:" + str(tweet_count) + '\n\n')



def clean_tweet(tweet): 
    """ This method cleans the tweets by removing links, special characters using
    simple regex statements.
    Args:
      tweet.... Tweet to be cleaned.
    Returns:
      cleaned tweet
    """
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())



def write_to_file():
    """ writes the summary of the collected data into a text file
    Args:
      Nothing
    Returns:
      the number of friends 
    """
    friends_data = pickle.load(open('./Collect Data/friends.pkl', 'rb'))

    friends_list = []
    for ids in friends_data.keys():
        friends_list.extend(friends_data[ids])
    friends_count = len(list(set(friends_list)))
    
    file = open('./Collect Data/collect_summary.txt', 'w')
    file.write("Number of users collected:" + str(friends_count + 1) + '\n\n')

    return friends_count 



def main():
    twitter = get_twitter()
    print("Twitter Connection Established")
    followers = find_friends(twitter, 'Cristiano' )
    count = write_to_file()
    print("Number of users collected:", count+1)
    tweets = get_tweets(twitter, 'Donald Trump')
    pass

if __name__ == "__main__":
    main()
