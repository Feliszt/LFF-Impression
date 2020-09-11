import tweepy
from keys import *
import json

# set username and tweet id
user_name = "@OrxraaRenz_"
tweet_id = 1291517343844245504

# authentification
auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

# get api object
api = tweepy.API(auth)

# get replies
replies = tweepy.Cursor(api.search, q='to:{}'.format(user_name), since_id=tweet_id, tweet_mode='extended').items()

# loop through replies
count = 0
while True:
    count = count + 1
    try:
        reply = replies.next()
        print("#{} - id {} replied to {} @ {}".format(count, reply.id, reply.in_reply_to_status_id, reply.created_at))
        if not hasattr(reply, 'in_reply_to_status_id_str'):
            continue
        if reply.in_reply_to_status_id == tweet_id:
           print("reply of tweet:{}".format(reply.full_text))

    except tweepy.RateLimitError as e:
        print("Twitter api rate limit reached".format(e))
        time.sleep(60)
        continue

    except tweepy.TweepError as e:
        print("Tweepy error occured:{}".format(e))
        break

    except StopIteration:
        break

    except Exception as e:
        print("Failed while fetching replies {}".format(e))
        break
