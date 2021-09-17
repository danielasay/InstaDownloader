# Import necessary libraries

import instaloader
import stdiomask
import os
import datetime as dt
from datetime import datetime
from itertools import dropwhile, takewhile
import time
import shutil as sh

# Create the post_downloader class

class post_downloader():
	def __init__(self):
		pass

	def login(self):
		# Create instance of the Instaloader class
		meme_bot = instaloader.Instaloader()

		# Get username and password from user
		while True:
			username = input("Enter your username: ")
			password = stdiomask.getpass()
			try:
				print("Logging into your Instagram account...")
				meme_bot.login(username, password)
			except instaloader.exceptions.BadCredentialsException:
				print("Incorrect password! Please try again.")
				time.sleep(2)
				continue
			except instaloader.exceptions.InvalidArgumentException:
				print("Incorrect username! Please try again.")
				time.sleep(2)
				continue
			else:
				break
		print("Successfully logged in!")
		time.sleep(1)


	# get the date range from the user


	def get_dates(self):
		while True:
			input_date = input("How far back do you want to see posts from? Please enter in format mm/dd/yyyy: ")
			today = dt.datetime.today()
			try:
				start_date = datetime.strptime(input_date, '%m/%d/%Y')
				if start_date > today:
					print("You put a date from the future! Please try again.")
					time.sleep(2)
					continue
			except ValueError:
				print("Invalid date entered! Please try again.")
				time.sleep(2)
				continue
			else:
				break

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

		return end_date, start_date

	# Download posts from the pages specified by user.

	def get_posts(self, end_date, start_date):
		meme_input = input("Now enter the names of the pages you want to see memes from, separated by spaces: ")
		pages = meme_input.split(' ')
		meme_bot = instaloader.Instaloader()
		work_dir = os.getcwd()
		print("Downloading posts between " + str(start_date) + " and " + str(end_date) + "...")
		today = dt.date.today()
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
		time.sleep(1)

		return dir_list


	# Sort the vidoes and photos into different directories

	def sort_media(self, dir_list):
		print("Sorting media...")
		time.sleep(1)
		work_dir = os.getcwd()
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
		time.sleep(1)
		print("Done!")





download_posts = post_downloader()

download_posts.login()

dates = download_posts.get_dates()

posts = download_posts.get_posts(dates[0], dates[1])

download_posts.sort_media(posts)








