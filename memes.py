# Import necessary libraries

import instaloader
import stdiomask
import os
import datetime as dt
from datetime import datetime
from itertools import dropwhile, takewhile
import time
import shutil as sh
from fpdf import FPDF

### Get cwd

work_dir = os.getcwd()

# Create instance of the Instaloader class

meme_bot = instaloader.Instaloader()

#Get username and password from user

username = input("Enter your username: ")
password = stdiomask.getpass()

# While in Beta, will hardcode username and password

#Get the names of the pages desired

meme_input = input("Great! Now enter the names of the pages you want to see memes from, separated by spaces: ")
pages = meme_input.split(' ')

# Get the start date for posts range from user, check for date validity

while True:
	input_date = input("How far back do you want to see posts from? Please enter in format mm/dd/yyyy: ")
	try:
		start_date = datetime.strptime(input_date, '%m/%d/%Y')
	except ValueError:
		print("Invalid date entered! Please try again.")
		time.sleep(2)
		continue
	else:
		break

# Ask the user if they want today to be the upper range. If today is used, change it to integer

while True:
	use_today = input("Do you want today to be the upper limit of your range? If so, type yes. \nIf not, please enter the date in mm/dd/yyyy format: ")
	if use_today == "yes" or use_today == "y" or use_today == "Yes" or use_today == "YES":
		today = dt.date.today()
		today = str(today)
		end_year = today[0:4]
		end_year = int(end_year)
		end_month = today[6:7]
		end_month = int(end_month)
		end_day = today[8:10]
		end_day = int(end_day)
		end_day = end_day + 1
		end_date = datetime(end_year, end_month, end_day)
		break
	elif use_today != "yes" or use_today != "y" or use_today != "Yes" or use_today != "YES":
		try:
			end_date = datetime.strptime(use_today, '%m/%d/%Y')
		except ValueError:
			print("Invalid input! Please try again.")
			time.sleep(2)
			continue
	else:
		break


#login to user's instagram account

print("Logging into your Instagram account...")

meme_bot.login(username, password)


### Get today's date and change it into an integer


## Show user the specified range

print("Downloading posts between " + str(start_date) + " and " + str(end_date) + "...")

time.sleep(2)

## Download posts and put them in their respective directories

dir_list = []

for name in range(len(pages)):
	new_dir = pages[name] + "_" + today
	os.makedirs(new_dir)
	dir_list.append(new_dir)
	posts = instaloader.Profile.from_username(meme_bot.context, pages[name]).get_posts()
	for post in takewhile(lambda p: p.date > start_date, dropwhile(lambda p: p.date > end_date, posts)):
		print(post.date)
		meme_bot.download_post(post, new_dir)

print("Finished downloading!")

# Give time between steps 

time.sleep(2)

print("Sorting media...")

time.sleep(2)

### Navigate to newly created directory and create new sub directories of all relevant media

for i in range(len(dir_list)):
	os.chdir(dir_list[i]) 
	os.makedirs("Captions")
	os.makedirs("Photos")
	os.makedirs("Videos")
	os.chdir(work_dir)


# Get list of all downloaded posts and turn them into strings. Move media to appropriate folders.

data_list = []

for j in range(len(dir_list)):
	os.chdir(dir_list[j])
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
	os.chdir(work_dir)

time.sleep(2)

print("Done! Enjoy!")

time.sleep(2)

