"""
date: March 3, 2018
author: @BrendanMoore42

Twitter bot that sends a message if there's a hype amount of viewers watching a smash tournament.

Runs on it's own droplet/server.

Requirements:
Python 3.6+
Tweepy

Updated Dec 17th:
Adding -> Smash Bros Ultimate
"""

from credentials import *
import tweepy
from tweepy import OAuthHandler

import os
import re
import json
import time

import urllib.request
from bs4 import BeautifulSoup

smash_games = ['Super Smash Bros. Melee', 'Super Smash Bros. for Wii U',
               'Super Smash Bros. Brawl', 'Super Smash Bros.',
               'Super Smash Bros. Ultimate']

def send_tweet(tweet):
    # Authenticates via API
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth)

    #sends tweet
    api.update_status(tweet)


def get_viewer_data():
    """
    Accesses json data from reddit smashbros stream - if error (too many requests, bad page, etc),
    will wait 10 minutes to check again until successful. If successful, appends data to file and
    continues
    """
    file_success = None

    while file_success is None:
        try:
            #Fetch site
            red = "https://www.reddit.com/r/smashbros/wiki/livestreams.json"

            #load site, soup it
            red_page = urllib.request.urlopen(red)
            red_soup = BeautifulSoup(red_page, 'html.parser')
            #Turn to text then to json
            red_step = str(red_soup)
            json2 = json.loads(red_step)

            # Write viewer data to file
            with open(f'smash_json.txt', 'w') as file:
                file.write(json2['data']['content_md'])
            file_success = 'Success!'
            return True

        except:
            print('Unsuccessful, trying in 10 minutes')
            time.sleep(600)
            pass

def sort_user_data():
    """
    Parses stream, streamer and view count from txt file, depending on count will send a tweet or
    wait 3 hours until next check.
    """

    checker = True

    #Sort data
    with open(f'smash_json.txt', 'r') as file:
        for line in file:
            l = ''
            l += line
            k = l.split('|')
            game = k[0]

            #Isolate view count
            #viewers = k[2:3]
            #Turn view count to strings
            view_count = ''.join(k[2:3])

            #Split stream to streamer
            stream_j = ''.join(k[1:2])
            streamer_s = stream_j.split(']')
            streamer = streamer_s[0]

            #Isolate stream link
            stream_search = re.search("(?P<url>https?://[^\s]+)", str(streamer_s))

            #Counts viewers and tweets if success
            if game in smash_games:

                if checker == True:
                    if 50000 < int(view_count) < 10000000:
                        tweet_to_send = f"Whoa! There are {view_count} viewers for {game} on {stream_search[0][:-3]} right now! Don't miss this one! #SmashBros #{streamer[1:]}"
                        print(tweet_to_send)
                        checker = False
                        send_tweet(tweet_to_send)
                    if 10000 < int(view_count) < 49999:
                        tweet_to_send = f"Holy cow! {view_count} viewers tuning into {stream_search[0][:-3]} to watch {game} right now! #SmashBros #{streamer[1:]}"
                        print(tweet_to_send)
                        checker = False
                        send_tweet(tweet_to_send)
                    if 7000 < int(view_count) < 9999:
                        tweet_to_send = f"Wow! Check out {game} with {view_count} other viewers on {stream_search[0][:-3]} right now! #SmashBros #{streamer[1:]}"
                        print(tweet_to_send)
                        checker = False
                        send_tweet(tweet_to_send)
                    if 5000 < int(view_count) < 6999:
                        tweet_to_send = f"Sweet! Join {view_count} others watching {game} on {stream_search[0][:-3]}! #SmashBros #{streamer[1:]}"
                        print(tweet_to_send)
                        checker = False
                        send_tweet(tweet_to_send)
                    # if 1501 < int(view_count) < 4999:
                    #     tweet_to_send = f"Looks like {view_count} viewers enjoying {game} on {stream_search[0][:-3]}! Let's go! #SmashBros #{streamer[1:]}"
                    #     print(tweet_to_send)
                    #     checker = False
                    #     send_tweet(tweet_to_send)
                    if int(view_count) < 4999:
                        print('No tweet sent...')
                        return True
                    else:
                        print('Something else happened...\n')
                        return True
                if checker == False:
                    print("Beep boop beep...\n")
                    checker = True


def main():
    """
    Looks for data, if found sends tweet based off view count,
    removes txt file for next loop after sleep.
    """

    while True:

        get_viewer_data()
        sort_user_data()

        print('Deleting smash_json.txt...')
        os.remove('smash_json.txt')

        print('Tweet sent, sleeping for 4 hours...')
        time.sleep(14400) #4 hours

if __name__ == '__main__':
    main()





