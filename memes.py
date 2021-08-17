# Import instaloader module

import instaloader
import stdiomask
import os
import datetime

# Create instance of the class

meme_bot = instaloader.Instaloader()

#Get username and password from user

#username = input("Enter your username: ")
#password = stdiomask.getpass()

# While in Beta, will hardcode username and password

username = input("Enter your username: ")
password = stdiomask.getpass()


#Get the names of the pages desired

user_input = input("Great! Now enter the names of the pages you want to see memes from, separated by spaces: ")
pages = user_input.split(' ')

meme_bot.login(username, password)

## Load profile

profile = instaloader.Profile.from_username(meme_bot.context, 'daquan')

#Get the posts

posts = profile.get_posts()


## Iterate through each post and download them

for index, post in enumerate(posts, 1):
	meme_bot.download_post(post, "daquan_" + str(datetime.date.today()))



