#!/usr/bin/python
import praw
import re
import os
import time
import string
from config import *
from functions import *
#See fucntions.py the majority of the imporant code

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

subreddit = r.get_subreddit('all')

excluded_subs = ["mistyfront",  "longtail", "AskElectronics"]; # Subs to ignore (most of the time I'm banned) 
split_punct = ["[",  "]", "(", ")", ".", "\'"]; #Punctuation marks that require the stripping of anything afterwards
other_bots = ["XPostLinker", "OriginalPostSearcher"]; #Bots that might already comments (so we ignore the post)

while True:
	for i in range(60,0,-1): # Search every 1 minutes
		os.system('clear')
		print("/u/TheLazyLinker:")
		print(str(i) + " seconds remaining till search")
		time.sleep(1)
	print("Searching...")
	for submission in subreddit.get_rising(limit=100): #get_top_from_hour or get_new
		# If we haven't replied to this post before
		if submission.id not in posts_replied_to:
			# Do a case insensitive search
			if re.findall(r"[^a-zA-Z0-9]r/([^\s/]+)", submission.title, re.IGNORECASE): # If the initial pattern exist in title
				subreddit_stripped = strip_subreddit(submission);

				posts_replied_to.append(submission.id) #Add to file
				# Now we can try to post
				if not is_post_ignored(submission):
					try: 
						submission.add_comment("Subreddit mentioned in the title: /r/" + subreddit_stripped + "\n\n \-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\- \n\n  *^^I'm ^^a ^^bot, ^^a ^^score ^^< ^^0 ^^deletes* \n\n ^^^[Code](https://github.com/braeden123/TheLazyLinker) ^^^[Contact](https://www.reddit.com/message/compose/?to=bsmith0)")
					except:
						print("exception")

	# Write our updated list back to the file
	with open("posts_replied_to.txt", "w") as f:
		for post_id in posts_replied_to:
			f.write(post_id + "\n")
	delete_low_comments(r); # Give praw to function



