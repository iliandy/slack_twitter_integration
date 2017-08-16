"""
Please refer to README.md for project description, usage, and requirements.
"""

# import required modules, libraries
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

# tweepy Listener class to actively listen for Twitter steams
class Listener(StreamListener):
    def on_data(self, raw_data):
        # convert tweet from unicode to json object and obtain tweet text
        tweet = json.loads(raw_data)
        tweet_to_slack_text = str(tweet["text"])

        # create slack msg from dict and convert to json object string, send POST request to Slack webhook URL
        slack_webhook_url = my_slack_webhook_url()
        slack_msg = json.dumps({"text": tweet_to_slack_text})
        req = requests.post(slack_webhook_url, slack_msg)

        # continue running on_data listener
        return True

    def on_error(self, status):
        print status

def oauthTwitter():
    # Twitter API app consumer key, consumer secret, access token, access secret
    ckey = my_ckey()
    csecret = my_csecret()
    atoken = my_atoken()
    asecret = my_asecret()

    # OAuth authenticate to connect to Twitter API
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)

    return auth

def index(request):
    # OAuth to Twitter API
    auth = oauthTwitter()

    # listen for Twitter streams with hashtag #wodedev (Slack channel name)
    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=["#wodedev"])

    return HttpResponse("twitterStream running...")

# bypass Django CSRF token verification, otherwise Slack slash commands are rejected with HTTP 403 code
@method_decorator(csrf_exempt)
def createTweet(request):
    # HTTP GET requests
    if request.method != "POST":
        return HttpResponse("/tweets route, GET request")

    # obtain text from Slack slash command msg object
    slack_to_twitter_text = request.POST.get("text", False)

    # OAuth to Twitter API
    auth = oauthTwitter()

    # post Slack tweet msg to Twitter
    api = API(auth)
    api.update_status("{}".format(slack_to_twitter_text))

    # respond to Slack slash command
    return HttpResponse("Successfully tweeted Slack msg to Twitter.")
