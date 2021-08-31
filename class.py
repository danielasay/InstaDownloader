# Import necessary libraries

import instaloader
import stdiomask
import os
import datetime as dt
from datetime import datetime
from itertools import dropwhile, takewhile
import time
import shutil as sh
import glob

# Create the post_downloader class

class post_downloader():
	def __init__(self):
		pass

	def login(self):
		# Create instance of the Instaloader class
		meme_bot = instaloader.Instaloader()
		# Get username and password from user
		username = input("Enter your username: ")
		password = stdiomask.getpass()
		#login to user's instagram account
		print("Logging into your Instagram account...")
		meme_bot.login(username, password)
		print("Successfully logged in!")
		time.sleep(2)


	def get_posts(self):
		#instance of instaloader
		meme_bot = instaloader.Instaloader()
		# Create the working directory
		work_dir = os.getcwd()
		#Get the names of the pages desired
		meme_input = input("Now enter the names of the pages you want to see memes from, separated by spaces: ")
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
				today = dt.date.today() + dt.timedelta(days=1)
				today = str(today)
				end_year = today[0:4]
				end_year = int(end_year)
				end_month = today[6:7]
				end_month = int(end_month)
				end_day = today[8:10]
				end_day = int(end_day)
				end_date = datetime(end_year, end_month, end_day)
				today = dt.date.today()
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
		print("Downloading posts between " + str(start_date) + " and " + str(end_date) + "...")
		time.sleep(2)
		## Download posts and put them in their respective directories
		dir_list = []
		for name in range(len(pages)):
			new_dir = pages[name] + "_" + str(today)
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
		## Go through Videos and Photos to check for any that match. If so, remove the Photo
		print("Removing video thumbnails...")
		video_timestamp = []
		for j in range(len(dir_list)):
			os.chdir(dir_list[j])
			page_dir = os.getcwd()
			os.chdir(page_dir)
			os.chdir("Videos")
			video_list = os.listdir()
			for i in video_list:
				video_timestamp.append(i[0:19])
			os.chdir(page_dir)
			os.chdir("Photos")
			for timestamp in range(len(video_timestamp)):
				for file in os.listdir():
					if file.startswith(video_timestamp[timestamp]):
						os.remove(file)
			os.chdir(work_dir)
		time.sleep(2)
		#change the photo extensions from jpg to png
		print("Modifying photo extensions...")
		photo_base = []
		for j in range(len(dir_list)):
			os.chdir(dir_list[j])
			page_dir = os.getcwd()
			os.chdir(page_dir)
			os.chdir("Photos")
			photo_list = os.listdir()
			for i in glob.glob("*.jpg"):
				os.rename(i, i[:-3] + "png")
			os.chdir(work_dir)

		time.sleep(2)
		print("Done! Enjoy!")
		time.sleep(2)



download_posts = post_downloader()

download_posts.login()

download_posts.get_posts()








