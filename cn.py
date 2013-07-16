# citation-needed by Izaak Baker (c) 2013
# prints to the console a (likely) false English statement created by 
# stitching together the first sentences of two random Wikipedia articles

import re
import urllib.request
import urllib.error
from bs4 import BeautifulSoup

# getLine returns the first sentence of a random wikipedia article, or
# 0 on failure
def getLine():
	# Create an opener
	opener = urllib.request.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	
	# Open a random page
	resource = opener.open("http://en.wikipedia.org/wiki/Special:Random")
	data = resource.read()
	resource.close()
	
	# Get the first paragraph
	soup = BeautifulSoup(data)
	try:
		line = soup.p.get_text()
	except:
		return 0
	
	# Get the first sentence
	line = re.sub("^b('|\")","",line)
	lmatch = re.match("(.*?\.) [A-Z]",line)
	
	# If the regex worked, return the sentence found
	if(lmatch):
		line = lmatch.group(1)
		return line
	else:
		return 0

# getHalf takes an integer (half) which, if zero means it will return everything
# up to the "is a", and otherwise everything after "is a."
def getHalf(half, line = 0, piece = 0, p_match = 0):
	# Retrieve a line
	# n = 0
	while(1):
		# n += 1
		if(not line):
			# print("Attempting to get half " + str(half) + ", attempt " + str(n) + "...")
			line = getLine()
		else:
			break
	
	# Slice the line in half
	if(not half):
		p_match = re.match("^(.*?) (is|was|are|were)", line)
	else:
		p_match = re.match("^(.*?) (is|was|are|were) (an|a|the) (.*)$", line)
	
	# Either grab the line pieces or, if the regex didn't work, call self again
	if(p_match):
		if(not half):
			piece = p_match.group(1,2)
		else:
			piece = p_match.group(3,4)
		piece = piece[0] + " " + piece[1]
	else:
		# print("Uh, oh! redoing half " + str(half) + "...")
		return getHalf(half)
	
	# Return the half found
	return piece

# TRY TRY AGAIN
def ifAtFirstYouDontSucceed():
	try:
		print(getHalf(0) + " " + getHalf(1))
	except UnicodeEncodeError:
		ifAtFirstYouDontSucceed()
	except urllib.error.URLError:
		print("Problem retrieving Wiki information... check your internet connection?")
	except:
		print("Man, something really awful happened...")

# Finally, here's the program :P
ifAtFirstYouDontSucceed()