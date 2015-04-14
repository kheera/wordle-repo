#!/usr/bin/python

# for easier web debugging, remove for production.
import cgitb
cgitb.enable()

# used for processing form data
import cgi

# used to download files from another site
import urllib2

# libraries for accessing filesystem
import tempfile
import zipfile
import os
import shutil

# calculates most frequent words, designs image
from wordcloud import WordCloud

# used for pattern matching
#import re

# to throw errors
import sys

# gets user data
form = cgi.FieldStorage()

# create location to store git archive
fdir = tempfile.mkdtemp()

giturl = form.getfirst('git', '')

#m = re.search('^https://github.com/', form.getfirst('git', ''))
if not (giturl.startswith("https://github.com") and giturl.endswith(".zip")):
	raise Exception("Invalid URL");
# download from url
response = urllib2.urlopen(form.getfirst('git', ''))
html = response.read()

# save the file so we can later unzip it
f = open(fdir + '/1.zip', 'w')
f.write(html)
f.close()

# need to extract the repo zip so we can create gigantic file containing all the words in the repo
myzip = zipfile.ZipFile(fdir+'/1.zip','r')
myzip.extractall(fdir+'/1/')

# get all the files we're interested in
# and concat them into one in memory variable
all_the_code = "1"
for root, dirs, files in os.walk(fdir+'/1/'):
	for file in files:
		#print os.path.join(root,file) + '<br><br>'
		filename, fileExt = os.path.splitext(file)
		if (fileExt in ['.js', '.php', '.c', '.cpp', '.asp', '.java', '.pl', '.py']):
			f = open(os.path.join(root,file), "r")
			all_the_code += f.read()		
			f.close()
# we're done with the download so remove it
shutil.rmtree(fdir)

# create tmp file to store wordle in
wordlefile = tempfile.NamedTemporaryFile(mode='w+b', dir='wordleimgs', prefix='img', suffix=".png",  delete=False)
mywordlename = os.path.relpath(wordlefile.name)

# creates wordcloud
words = WordCloud(width=750, height=500, font_path='/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf')
words.generate(all_the_code)
words.to_file(wordlefile)

wordlefile.close()

# redirects to saved wordcloud image
print "Location: " + mywordlename + "\n\n"
