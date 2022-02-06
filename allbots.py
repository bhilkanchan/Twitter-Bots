import tweepy
import time
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["API_KEY"]
API_KEY_SECRET = os.environ["API_KEY_SECRET"]
ACCESS_TOKEN = os.environ["ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

countfollow = 0
countmessage = 0
requestcount = 0

#Add your username here
myusername = "" 
#Customize the message
messagetext = "Hey" 

# bot to follow and message users who tweet in a specific area
def followmessage(querytext, geocodetext):
    global countmessage
    global countfollow
    global requestcount
    # use cursor to divide the results in 100 per page
    cursor = tweepy.Cursor(api.search_tweets, q=querytext, geocode=geocodetext) 
    for page in cursor.pages(20):
        for tweet in page:
            try:
                if(requestcount <= 99000):
                    # Get the friendship status between you and the user
                    friendship = api.get_friendship(source_screen_name=myusername, target_screen_name=tweet.user.screen_name)
                    requestcount = requestcount+1

                    # Check that you are not following the user and user's messaging option is open
                    if(friendship[0].following == False and countfollow <= 950 and friendship[0].can_dm == True):
                        api.create_friendship(screen_name=tweet.user.screen_name)
                        requestcount = requestcount+1

                        print("Request count is:", requestcount)
                        print("followed:", tweet.user.screen_name)

                        countfollow = countfollow+1
                        print('Follow count:', countfollow)

                        api.send_direct_message(recipient_id=tweet.user.id, text=messagetext)
                        requestcount = requestcount+1

                        print("Request count is:", requestcount)
                        print("sent message to:", tweet.user.screen_name)

                        countmessage = countmessage+1
                        print('Message count:', countmessage)
                    time.sleep(20)
                else:
                    break
            except tweepy.HTTPException as e:
                print(e)
                if(e.api_codes == 226):
                    time.sleep(600)
                else:
                    time.sleep(5)


countlike = 0

# bot to like the tweets of users with specific words
def liketweetbot(querytext):
    global countlike
    global requestcount
    for tweet in api.search_tweets(q=querytext):
        try:
            if(requestcount <= 99000):
                tweetid = api.get_status(tweet.id)
                requestcount = requestcount+1

                if(tweetid.favorited == False and countlike < 950):
                    api.create_favorite(tweet.id)
                    requestcount = requestcount+1

                    print("Request count is:", requestcount)
                    print("Liked tweet of user:", tweet.user.screen_name)

                    countlike = countlike+1
                    print('Tweet like count:', countlike)
                time.sleep(30)
            else:
                break
        except tweepy.HTTPException as e:
            print(e)
            if(e.api_codes == 226):
                time.sleep(600)
            else:
                time.sleep(5)


countretweet = 0

# bot to retweet the tweets of users with specific words
def retweetbot(querytext):
    global countretweet
    global requestcount
    for tweet in api.search_tweets(q=querytext):
        try:
            if(requestcount <= 99000):
                setretweeted = api.get_status(tweet.id)
                requestcount = requestcount+1
                if(setretweeted.retweeted == False and countretweet < 950):
                    api.retweet(tweet.id)
                    requestcount = requestcount+1

                    print("retweeted", tweet.id)
                    countretweet = countretweet+1
                time.sleep(60)
            else:
                break
        except tweepy.HTTPException as e:
            print(e)
            if(e.api_codes == 226):
                time.sleep(600)
            else:
                time.sleep(5)


def main():
    followmessage(" ", "40.730610,-73.935242,5mi")
    time.sleep(300)


if __name__ == "__main__":
    main()

# Insert query to like the tweet
liketweetbot(" ")
time.sleep(100)

# Insert query to retweet the tweet
retweetbot(" ")
time.sleep(100)


print("message count:", countmessage, date.today())
print("follow count:", countfollow, date.today())
print("Like count:", countlike, date.today())
print("retweet count:", countretweet, date.today())
