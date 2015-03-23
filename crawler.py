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
			return
			
		if self.depth <= self.max_depth:
			print("Current depth level: ", self.depth)
		
			for link in self.br.links():
				self.links.append(link)
			
				if link not in self.visited_links:
					print('Link to follow: ', link.text)
					response = self.br.follow_link(link)
					self.depth += 1
					
					print(response.code)
					self.results += str(response.code)
					
					self.visited_links.append(link)
					print("Current url: ", self.br.geturl())
				
					self.crawl_all_links()
					self.br.back()
					self.depth -= 1
					print("Going back")
				
		#print('All visited links: ')
		for link in self.links:
			print("Links: ", link.text)
			
'''url = 'http://www.example.com'
crawler = Crawler(url)
crawler.crawl_all_links()'''
