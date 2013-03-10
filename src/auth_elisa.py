import tweepy
from tweepy import OAuthHandler

def set_consumer_key():
    #OAuth 
    consumer_key = ""
    consumer_secret = ""
    Auth= tweepy.OAuthHandler(consumer_key,consumer_secret)
    return Auth

def set_access_token(auth):
    access_token = ""
    access_token_secret = ""
    auth.set_access_token(access_token,access_token_secret)
    return auth


def get_API(auth):
    return tweepy.API(auth)

def print_name(api):
    #If the authentication succeed , it is able to print the app name
    print api.me().name + " authenticated successfully"


    
    
