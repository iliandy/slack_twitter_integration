# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
from tweepy.utils import import_simplejson
import requests
from secrets import *

json = import_simplejson()
class listener(StreamListener):
    def on_data(self, raw_data):
        tweets = json.loads(raw_data)
        tweet_to_slack_text = str(tweets["text"])

        slack_webhook_url = "https://hooks.slack.com/services/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"
        slack_msg = json.dumps({"text": tweet_to_slack_text})
        req = requests.post(slack_webhook_url, slack_msg)

        print tweet_to_slack_text
        print req.status_code, req.reason

        return True

    def on_error(self, status):
        print status

def index(request):
    print "-= Reached / (index.html) =-"

    #consumer key, consumer secret, access token, access secret
    ckey = my_ckey()
    csecret = my_csecret()
    atoken = my_atoken()
    asecret = my_asecret()

    # OAuth authenticate to connect to Twitter API
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    # listen for Twitter streams with hashtag #wodedev
    twitterStream = Stream(auth, listener())
    twitterStream.filter(track=["#wodedev"])

    return HttpResponse("twitterStream running...")

@method_decorator(csrf_exempt)
def createTweet(request):
    if request.method == "POST":
        slack_to_twitter_text = request.POST.get("text", False)

        # file = open("my_django_logs.txt", "w")
        # file.write("{}".format(slack_to_twitter_text))
        # file.close()

        # consumer key, consumer secret, access token, access secret
        ckey = my_ckey()
        csecret = my_csecret()
        atoken = my_atoken()
        asecret = my_asecret()

        # OAuth authenticate to connect to Twitter API
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)

        # post Slack Tweet text to Twitter
        api = API(auth)
        api.update_status("{}".format(slack_to_twitter_text))

        # continue listening for Twitter streams with hashtag #wodedev
        return redirect("/")

    # request.method == "GET"
    else:
        return HttpResponse("/tweets GET route...")
