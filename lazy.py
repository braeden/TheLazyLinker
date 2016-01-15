#!/usr/bin/python
import praw
import sys
import pdb
import re
import math
import os
import time
import datetime
import string
import subprocess
from config import *

# Check that the file that contains our username exists
if not os.path.isfile("config.py"):
    print("You must create a config file with your username and password.")
    exit(1)

# Create the Reddit instance
user_agent = ("TheLazyLinker v0.1a")
r = praw.Reddit(user_agent=user_agent)

# and login
r.login(REDDIT_USERNAME, REDDIT_PASS)

# Have we run this code before? If not, create an empty list
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

# If we have run the code before, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
	with open("posts_replied_to.txt", "r") as f:
		posts_replied_to = f.read()
		posts_replied_to = posts_replied_to.split("\n")


# Get the top 5 values from our subreddit
subreddit = r.get_subreddit('all')
excluded_subs = ["mistyfront",  "longtail", "AskElectronics"];
while True:
	for i in range(60,0,-1): # Search every 1 minutes
		os.system('clear')
		print("/u/TheLazyLinker: \n")
		sys.stdout.write(str(i)+' ')
		print("seconds remaining till search")
		time.sleep(1)
	print("Searching...")
	for submission in subreddit.get_rising(limit=100): #get_top_from_hour
		# If we haven't replied to this post before
		if submission.id not in posts_replied_to:

			# Do a case insensitive search
			if re.findall(r"[^a-zA-Z0-9]r/([^\s/]+)", submission.title, re.IGNORECASE): # If the initial pattern exist in title
				subreddit_link = re.findall(r"[^a-zA-Z0-9]r/([^\s/]+)", submission.title, re.IGNORECASE) # Put intial pattern matches into string 
				subreddit_some_punct = re.sub(r"[^a-zA-Z0-9_'\.\]\)]", "", subreddit_link[0]) # Strip punctiation except a few cases _ and things that require the deleteion of the rest of the string
				subreddit_some_punct = subreddit_some_punct.split(']', 1)[0] # Only take the first part after enountering char
				subreddit_some_punct = subreddit_some_punct.split(')', 1)[0] # ^
				subreddit_stripped= subreddit_some_punct.split('.', 1)[0]    # ^
				if str(submission.subreddit).lower() != subreddit_stripped.lower(): # Not referencing the subreddit its posted in
					posts_replied_to.append(submission.id) #Add to file
					ignore_post = False
					#					
					## Couple of instances to ignore post
					#
					for sub in excluded_subs: 
						if str(submission.subreddit).lower() == sub.lower():
							ignore_post = True
							# Excluded subs that have not banned me
					if not submission.is_self and 'r/'+subreddit_stripped.lower() in submission.url.lower():
						ignore_post = True
						# Submission links to the mentioned subreddit
					if 'r/'+subreddit_stripped.lower() in submission.selftext.lower():
						ignore_post = True
						# Self text contains the subreddit
					flat_comments = praw.helpers.flatten_tree(submission.comments)
					for comment in flat_comments: # ignores the post if either user has already commented
						if comment.author is not None:
							if (comment.author.name == "XPostLinker") or (comment.author.name == "OriginalPostSearcher"):
								ignore_post = True
								# Other bot beat me too it
						if 'r/'+subreddit_stripped.lower() in comment.body.lower():
							ignore_post = True
							# Subreddit is mentioned in one of the comments

					# Now we can try to post
					if not ignore_post:
						try: 
							submission.add_comment("Subreddit mentioned in the title: /r/" + subreddit_stripped + "\n\n \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \n\n  *^^I'm ^^a ^^bot, ^^a ^^score ^^< ^^0 ^^deletes* \n\n ^^^[Code](https://github.com/braeden123/TheLazyLinker) ^^^[Contact](https://www.reddit.com/message/compose/?to=bsmith0)")
						except:
							print("exception")

						log = open('log.txt', 'a') # Write comment details to log file
						log.write("Bot replying to : " + submission.title + "\n")
						log.write("Link: " + submission.url + "\n")
						log.close()

	# Write our updated list back to the file
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")
	user = r.get_redditor('TheLazyLinker')
	for comment in user.get_comments(limit=None): #None
	  if (comment.score < 0):
	    comment.delete() # Check through all comments to delete them if score <0