# Intro
This Tool takes as input a list of URLs, and which outputs, for each URL, a score indicating if remote website is using Ruby on Rails

# Examples:

	$./testRoR.py http:// sqreen.io/ http://a_ror_website.fake/
	
	score	URL
	1/5	http://sqreen.io/
	5/5	http://a_ror_website.fake/

	$./testRoR.py -f examples_urls.txt		# List all score of URL in file
	$./testRoR.py --help			# Display this file
	
To ADD more heuristics, you just have to search the isRoR() function in testRoR class and add your code in. 
