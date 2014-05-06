import tweepy
import pickle
import dropbox
import time
import math
 
#+++++++
# this code runs via cron 10 times per day. crontab entries look like:
#  0 9 * * * python /home/pi/twainbot/twain_bot.py
#
# all paths full to run on RaspberryPi w/ cron
#+++++++


### read in the list of tweets, already defined in MOCK_PREP.py
tweet_file = open('/home/pi/twainbot/tweet_list.pkl','rb')
tweet_list = pickle.load(tweet_file)
tweet_file.close()

### figure out which to send (read in iterator file)
num = int(open('/home/pi/twainbot/tweetnumber.txt').read())

### send tweet!
### The Twitter-Posting Script... ###
CONSUMER_KEY = 'mykey'
CONSUMER_SECRET = 'mysecret'

ACCESS_KEY = 'myaccesskey'
ACCESS_SECRET = 'myaccesssecret'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

### tweet relavent post  (if not at end)
if num+1 <= len(tweet_list):
    if len(tweet_list[num]) <= 140: # normal tweet, works 99% of time
        api.update_status(tweet_list[num])
    elif len(tweet_list[num]) > 140: # split if over 140char, rare
        ww = tweet_list[num].split(' ')
        lw = len(ww)
        api.update_status(' '.join(ww[0:int(math.floor(lw/2))]))
        time.sleep(5)
        api.update_status(' '.join(ww[int(math.floor(lw/2)):]))


### update post schedule number file
    num = num+1
    outnum = open('/home/pi/twainbot/tweetnumber.txt','w').write(str(num))

### query for # followers, write to a local file
    with open('/home/pi/twainbot/numfollow.txt','a') as numfollow:
        numfollow.write(str(len(api.followers_ids())) + '\n')

### keep timestamp local file
    with open("/home/pi/twainbot/times.txt", "a") as timefile:
        timefile.write(time.ctime() + '\n')


######## update these files via dropbox so I can keep an eye
#        on the status while traveling, push updates if needed
db_APP_KEY = 'mydropboxkey'
db_APP_SECRET = 'mydropboxsecret'
db_access_token = u'myaccesstoken'

client = dropbox.client.DropboxClient(db_access_token)
fnum = open('/home/pi/twainbot/tweetnumber.txt','r')
r1 = client.put_file('/tweetnumber.txt',fnum,overwrite=True)

ftime = open('/home/pi/twainbot/times.txt','r')
r2 = client.put_file('/times.txt', ftime,overwrite=True)

ffol = open('/home/pi/twainbot/numfollow.txt','r')
r3 = client.put_file('/numfollow.txt', ffol, overwrite=True)

