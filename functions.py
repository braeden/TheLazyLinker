def is_post_ignored(submission):
	if str(submission.subreddit).lower() == subreddit_stripped.lower():
			return(True)
			# Mentions the sub its posted in

	for sub in excluded_subs: 
		if str(submission.subreddit).lower() == sub.lower():
			return(True)
			# Excluded subs that have not banned me

	if not submission.is_self and 'r/'+subreddit_stripped.lower() in submission.url.lower():
		return(True)
		# Submission links to the mentioned subreddit

	if 'r/'+subreddit_stripped.lower() in submission.selftext.lower():
		return(True)
		# Self text contains the subreddit

	flat_comments = praw.helpers.flatten_tree(submission.comments)
	for comment in flat_comments: # ignores the post if either user has already commented
		if comment.author is not None:
			for bot in other_bots: 
				if comment.author.name == bot:
					return(True)
					# Other bot beat me too it

		if 'r/'+subreddit_stripped.lower() in comment.body.lower():
			return(True)
			# Subreddit we found is mentioned in one of the comments
	return(False);


def delete_low_comments():
	user = r.get_redditor('TheLazyLinker')
	for comment in user.get_comments(limit=None):
	  if (comment.score < 0):
	    comment.delete() # Check through all comments to delete them if score <0


def strip_subreddit(submission):
	subreddit_link = re.findall(r"[^a-zA-Z0-9]r/([^\s/]+)", submission.title, re.IGNORECASE) # Put intial pattern matches into string 
	subreddit_some_punct = re.sub(r"[^a-zA-Z0-9_'\.\[\]\(\)]", "", subreddit_link[0]) # Strip punctiation except a few cases _ and things that require the deleteion of the rest of the string
	
	for punct in split_punct:
		subreddit_some_punct = subreddit_some_punct.split(punct, 1)[0]	# Only take the first part after enountering char
	return(subreddit_some_punct)