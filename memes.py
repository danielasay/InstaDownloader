# Import instaloader module

import instaloader
import stdiomask
import os
import datetime as dt
from datetime import datetime
from itertools import dropwhile, takewhile
import time
import shutil as sh

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

print("Logging into your Instagram account...")

meme_bot.login(username, password)

## Load profile and get the posts

posts = instaloader.Profile.from_username(meme_bot.context, pages[0]).get_posts()

# Get the start date for posts range from user

#input_date = input("How far back do you want to see posts from? Please enter in format mm/dd/yyyy: ")

### Get today's date and change it into an integer

today = dt.date.today()
today = str(today)
end_year = today[0:4]
end_year = int(end_year)

end_month = today[6:7]
end_month = int(end_month)

end_day = today[8:10]
end_day = int(end_day)
end_day = end_day + 1

## populate range of dates

start_date = datetime(2021, 8, 22)


end_date = datetime(end_year, end_month, end_day)


## Check the date of each post and download the posts that are in appropriate range

print("Downloading posts between " + str(start_date) + " and " + str(end_date) + "...")

time.sleep(4)

for post in takewhile(lambda p: p.date > start_date, dropwhile(lambda p: p.date > end_date, posts)):
    print(post.date)
    meme_bot.download_post(post, pages[0] + str(dt.date.today()))

print("Finished downloading!")

### Navigate to newly created directory and create new sub directories

time.sleep(2)

print("Sorting media...")

time.sleep(2)

os.chdir("upworthy2021-08-23") ### make this dynamic
os.makedirs("Captions")
os.makedirs("Photos")
os.makedirs("Videos")

# Get list of all downloaded posts and turn them into strings

data_list = os.listdir()

for i in data_list:
	i = str(i)
	extension = i[-3:]
	if extension == "mp4":
		sh.move(i, "Videos")
	elif extension == "jpg":
		sh.move(i, "Photos")
	elif extension == "txt":
		sh.move(i, "Captions")
	elif extension == ".xz":
		os.remove(i)



print("Done!")











