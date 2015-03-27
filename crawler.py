import mechanize

class Crawler():
	
	br = mechanize.Browser()
	max_depth = 10 
	depth = 0
	visited_links = []
	links = []
	avoided_links = []
	results = {}
			
	def __init__(self, url):
		self.url = url
		# try to open the base URL
		try:
			self.opening = self.br.open(self.url)
		except Exception as e:
			print('Exception: ', e)
			self.results['base url'] = str(e)
			self.opening = None

	def crawl_all_links(self, max_depth):
		
		# if base URL is successfully opened, proceed
		if self.opening != None:
			pass
		else:
			#print("self.opening is None", self.opening)
			return
		
		# while the depth is not higher than maximum depth level
		if self.depth <= max_depth: 
					
			# collect all the links in the current url
			for link in self.br.links():
				#print("current depth level: ", self.depth)
				#print("current URL: ", self.br.geturl())
				#print("next link: ", link.url)
								
				# if the links are not in the visited_links or avoided_links lists, add them to the links list.
				if link not in self.visited_links and link not in self.avoided_links:
					self.links.append(link)
			
			# for each link in the links list
			#for link in self.links:
				
			# if it's an outside link, put it in the avoided_links list.
			if (self.links[0].url[:4] == 'http' and self.links[0].url[:len(self.url)] != self.url) or ('youtube' in self.links[0].url):
				self.avoided_links.append(self.links[0])
				#print('avoided_links: ', self.avoided_links)
							
			# if the link is not in the visited_links or avoided_links lists,					
			if self.links[0] not in self.visited_links and self.links[0] not in self.avoided_links:
				#print(link.url[:4], link.url[:len(self.url)], self.url, link.url)
									
				# open the link	
				response = None
				try:
					response = self.br.follow_link(self.links[0])
					print("this is the link: ", self.links[0].url)
				except Exception as e:
					self.results[self.links[0].url] = str(e)
		
				# if the link is successfully opened,
				if response != None:
					print("current url: ", self.br.geturl())
					# add the link to visited_links list
					self.visited_links.append(self.links[0])
					# delete the first item in the links list
					self.links.pop(0)
					# increase depth value by 1
					self.depth += 1
					# get the result in the res dictionary, add the response code to it.
					self.results[self.br.geturl()] = response.code
						
					# start this function again
					self.crawl_all_links(self.depth)
				else:
					self.crawl_all_links(self.depth)
				
		else:
			print('Done')
												
					
'''url = "http://www.example.com"
crawler = Crawler(url)
crawler.crawl_all_links()'''
