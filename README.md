Slack Twitter Integration Project

Description:
Built Slack Twitter Integration using Python Django and tweepy library. When a Twitter tweet with hashtag #wodedev posts, it will automatically be forwarded to Slack "wo_de_dev" #general channel. Conversely, when a Slack message with /tweets sends, it will automatically be forwarded and post to my Twitter feed.

Usage:
Django server acting as bridge between Slack and Twitter is deployed onto an Amazon EC2 instance with IPv4 address: http://34.203.28.178.
- For Twitter to Slack messaging, go to URL: http://34.203.28.178/ and make sure it's loading/running. The server will eventually timeout after constantly listening for Twitter streams and will need to be reloaded for bridging functionality to resume. Posting a tweet with hashtag #wodedev will be forwarded to Slack "wo_de_dev" channel.
- For Slack to Twitter messaging, functionality works successfully as long as server is not timed out. Slack slash command will send message as POST request to http://34.203.28.178/tweets. Sending a Slack message from "wo_de_dev" channel with /tweets will be forwarded to Twitter feed.

Requirements:
1. Created Twitter API app and generated access tokens. Used App Consumer Key (API Key), Consumer Secret (API Secret), Access Token, Access Token Secret to authenticate using OAuth 1.0 to access Twitter API.
2. Created Slack API app, activated incoming webhooks and slash commands features for incoming and outgoing messages to Twitter, respectively.
3. Bridging functionality between services is limited to Slack "wo_de_dev" #general channel and my Twitter account.
