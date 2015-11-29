#!/usr/bin/python

#######################################################
# Thomas AUBIN
# 28/11/2015
# This Tool takes as input a list of URLs, 
# and which outputs, for each URL, a score 
# indicating if remote website is using Ruby on Rails 
#######################################################


import requests
import os
import sys
import re
import warnings

# comment for debug
warnings.filterwarnings('ignore', '',)

class testRoR:
	"""
        This class takes as imput an URL. Use the function isRoR
        to know if the website is using Ruby on Rails.
        
        Example :
			testurl = testRoR("http://www.google.com)
			score = testurl.isRoR()
			return 1/5

    """ 
	def __init__(self, URL):
		self.URL = URL
		self.score = 0
		
	def check_URL(self):
		"""
			check if the URL exist and collect source and header.
		"""
		if self.verify_URL() == False:
			return False
		
		try:
			r = requests.get(self.URL)
		except:
			warnings.warn("error : fail request")
			return False
		if r.status_code >= 400:
			warnings.warn("error : error Status")
			return False
			
		self.page_source = r.iter_lines()
		self.info = r.headers
		
		self.score = 1
		
		return True
	
	def verify_URL(self):
		"""
			return True if we have a good URL
			False else
		"""
		if re.match(r'^https?:\/\/([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$', self.URL) == None:
			warnings.warn("error : URL format :" + self.URL)
			return False
		return True
		
	def printSource(self):
		"""
			display headers and source about the website
		"""
		print(self.URL)
		print(self.info)
		print(self.page_source)
		
	def isRoR(self):
		"""
			return a score between 0 and 5.
			0 if the website desn't use RoR.
			5 if the website use RoR
			return -1 if error
		"""
		if self.check_URL() == False:
			return -1
		
		######## Check in HTTP response headers ########
		if 'X-Powered-By' in self.info :
			if re.search(r'PHP', self.info['X-Powered-By']):
				return '0/5'
			elif re.search(r'rails', self.info['X-Powered-By']) :
				self.score += 2
		if 'server' in self.info :
			if re.search(r'rails', self.info['server']):
				self.score += 2
		#~ ADD heuristics :
		#~ if NAME_HEADER in self.info :
			#~ if re.search(r'REGEX', self.info['NAME_HEADER']):
				#~ self.score += SCORE
				
		######## Check in source code ########
		in_html_tag = False # True if between <html> and </html>
		for line in self.page_source:
			if re.search(r'<html', line):
				in_html_tag = True
			if re.search(r'</html>', line):
				in_html_tag = False
			if re.search(r'<meta.*content="Rails', line) and in_html_tag:
				self.score += 1
			if re.search(r'<meta.*name="csrf-param"', line) and in_html_tag:
				self.score += 2
			if re.search(r'<meta.*name="csrf-token"', line) and in_html_tag :
				self.score += 2
		#~ ADD heuristics :
			#~ if re.search(r'YOUR REGEX', line) :
				#~ self.score += SCORE
		
		######## Check urls and file extension #######
		# TO DO :
		
		####### return score #######
		if self.score > 5 :
			self.score = 5 
		
		return '' + str(self.score) + '/5'
		
	
		
		
def main():
	if len(sys.argv) < 2 :
		print("Try 'tar --help' for more information.")
		exit(-1)
	
	if re.match(r'--help$',sys.argv[1]):
		f = open('README.md','r')
		print(f.read())
		f.close()
		exit(1)
	
	print("score	URL")
	if re.match(r'-f$',sys.argv[1]) and len(sys.argv) == 3:
		filename = sys.argv[2]
		try:
			file_URL = open(filename,'r')
		except:
			print "Unexpected error:", sys.exc_info()[0]
			exit(-1)
		for url in file_URL.readlines():
			url = url.rstrip()
			if url != '':				
				testurl = testRoR(url)
				score = testurl.isRoR()
				if score == -1:
					print("Error	" + url)
				else:	
					print(score + "	" + url)
		
	else:
		for url in sys.argv[1:]:
			testurl = testRoR(url)
			score = testurl.isRoR()
			if score == -1:
				print("Error	" + url)
			else:	
				print(score + "	" + url)
	
main()
