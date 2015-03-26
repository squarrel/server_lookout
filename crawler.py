import mechanize

class Crawler():
	
	br = mechanize.Browser()
	visited_links = []
	max_depth = 10 
	depth = 0
	results = ''
	links = []
	res = {}
	avoided_links = []
		
	def __init__(self, url):
		self.url = url
		# try to open the base URL
		try:
			self.opening = self.br.open(self.url)
		except Exception as e:
			print('Exception: ', e)
			self.results = str(e)
			self.opening = None

	def crawl_all_links(self, max_depth):
		
		'''# if base URL is successfully opened, proceed
		if self.opening != None:
			pass
		else:
			#print("self.opening is None", self.opening)
			return'''
		
		if self.depth <= max_depth: 
			#print("Current depth level: ", self.depth)
		
			# collect all the links
			for link in self.br.links():
				if link not in self.visited_links:
					self.links.append(link)
			
			for link in self.links:
				if link not in self.visited_links and link not in self.avoided_links:
					if link.url[:4] == 'http' and link.url[:24] != self.url:
						self.avoided_links.append(link)
						print('Outside link: ', link.url)
						return
						
					response = None
					try:
						response = self.br.follow_link(link)
						#print(response)
					except Exception as e:
						self.results += link.url + ': ' + 'Exception: ' + str(e) + '\n'
		
					if response != None:
						print("Current URL: ", self.br.geturl())
						self.visited_links.append(link)
						self.links.pop(0)
						self.depth += 1
						self.res[self.br.geturl()] = response.code
				
						self.crawl_all_links(self.depth)
				
		else:
			print(self.results)
			

									
					
'''url = "http://www.example.com"
crawler = Crawler(url)
crawler.crawl_all_links()'''
