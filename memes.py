# Import instaloader module

import instaloader
import stdiomask
import os
import datetime as dt
from datetime import datetime
from itertools import dropwhile, takewhile

# Create instance of the class

meme_bot = instaloader.Instaloader()

#Get username and password from user

username = input("Enter your username: ")
password = stdiomask.getpass()

# While in Beta, will hardcode username and password


#Get the names of the pages desired

meme_input = input("Great! Now enter the names of the pages you want to see memes from, separated by spaces: ")
pages = meme_input.split(' ')

#login to user's instagram account

meme_bot.login(username, password)

## Load profile and get the posts

posts = instaloader.Profile.from_username(meme_bot.context, pages[0]).get_posts()

# Get the start date for posts range from user

input_date = input("How far back do you want to see posts from? Please enter in format mm/dd/yyyy: ")

### Get today's date and change it into an integer

today = dt.date.today()
today = str(today)
end_year = today[0:4]
end_year = int(year)

end_month = today[6:7]
end_month = int(month)

end_day = today[8:10]
end_day = int(day)

## populate range of dates

start_date = datetime(2021, 8, 15)


end_date = datetime(end_year, end_month, end_day)


## Check the date of each post and download the posts that are in appropriate range

for post in takewhile(lambda p: p.date > start_date, dropwhile(lambda p: p.date > end_date, posts)):
    print(post.date)
    meme_bot.download_post(post, pages[0] + str(dt.date.today()))


























