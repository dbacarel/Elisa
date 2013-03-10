import tweepy
from tweepy import OAuthHandler

def set_consumer_key():
    #OAuth 
    consumer_key = "yRUjyLvZUxIYlkCQdm2pQ"
    consumer_secret = "zsbTIIuma2CLRIG9eq6zAYwHLdMw6x3WfaMBPKMhtSg"
    Auth= tweepy.OAuthHandler(consumer_key,consumer_secret)
    return Auth

def set_access_token(auth):
    access_token = "305859183-EnKfk6f00xHZ7k8AZRSUT1NYNZJwIb9WKyDCk2k"
    access_token_secret = "C5oPHAcbWWrL9AZlWsNAtoS3I5rz7hXmnJgDxUg1M"
    auth.set_access_token(access_token,access_token_secret)
    return auth


def get_API(auth):
    return tweepy.API(auth)

def print_name(api):
    #If the authentication succeed , it is able to print the app name
    print api.me().name + " authenticated successfully"


    
    
