import mechanize

class Crawler():
	
	br = mechanize.Browser()
	links = []
	visited_links = []
	max_depth = 10
	depth = 0
	results = ''
		
	def __init__(self, url):
		self.url = url
		# try to open the base URL
		try:
			self.opening = self.br.open(self.url)
		except Exception as e:
			print('Exception: ', e)
			self.results = str(e)
			self.opening = None

	def crawl_all_links(self):
		
		# if base URL is successfully opened, proceed
		if self.opening != None:
			pass
		else:
			#print("self.opening is None", self.opening)
			return
		
		# limit the amount of depth with the max_depth variable.
		if self.depth <= self.max_depth:
			#print("Current depth level: ", self.depth)
		
			for link in self.br.links():
				self.links.append(link)
				
			for i in xrange(len(self.links)):
				link = self.links[i]
				response = None
			
				# some links are not recognized by the mechanize module? Hence the link.text != None condition, so as to not get stuck on some of them.
				if link not in self.visited_links and link.text != None \
					and link.url[:1] != '#' and link.url[:10] != 'javascript':
					
					print('Link to follow: ', link.text, link.url)
					
					# attempt to open the link
					try:
						response = self.br.follow_link(link)
					except Exception as e:
						self.results += link.text + ': ' + 'Exception: ' + str(e) + '\n'
											
					if response != None:
						self.depth += 1
						print("Response code: ", response.code)
						self.results += link.text + ': response ' + str(response.code) + '\n'
						# mark this link as a visited one, by placing it in the visited_links list.
						self.visited_links.append(link)
						self.br.back()
						self.depth -= 1
						print("Going back")
						print("Current location: ", self.br.geturl())
					else:
						self.results += link.text + link.url + ": couldn't open the link" + '\n' 
						print("Current location: ", self.br.geturl())
														
					self.crawl_all_links()
				
					
'''url = "http://www.example.com"
crawler = Crawler(url)
crawler.crawl_all_links()'''
