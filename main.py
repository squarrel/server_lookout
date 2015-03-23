__version__ = '0.11'

import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.storage.jsonstore import JsonStore

import paramiko
from crawler import Crawler

class Root(Widget):

	store = JsonStore('storage.json')
	server_url = StringProperty(store.get('server_url')['value'])
	username = StringProperty(store.get('username')['value'])
	password = StringProperty('')
	#connection_status = StringProperty('')
	website = StringProperty(store.get('website')['value'])
	messages = StringProperty('')
	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	
	def connect(self):
		try:
			self.ssh.connect(self.server_url, username=self.username, password=self.password)
		except Exception as e:
			print('Exception connecting to the server: ', e)

	def check_memory(self):
		try:
			stdin, stdout, stderr = self.ssh.exec_command("free -m")
			rl = stdout.readlines()
			self.messages = ''
			for line in rl:
				self.messages += line
		except Exception as e:
			print('Exception executing command: ', e)
			# print the error to the output screen
			m = 'Exception executing command: ' + str(e)
			self.messages = m
					
	def list_folders(self):
		try:
			stdin, stdout, stderr = self.ssh.exec_command("ls")
			rl = stdout.readlines()
			self.messages = ''
			for line in rl:
				self.messages += line
		except Exception as e:
			print('Exception executing command: ', e)
			m = 'Exception executing command: ' + str(e)
			self.messages = m

	def url_to_storage(self, data):
		self.store.put('server_url', value=data.text)
		self.server_url = data.text
		
	def username_to_storage(self, data):
		self.store.put('username', value=data.text)
		self.username = data.text
		
	def password_to_storage(self, data):
		self.password = data.text
		
	def website_to_storage(self, data):
		self.store.put('website', value=data.text)
		self.website = data.text
	
	def crawl(self):
		#print('self.website: ', self.website)
		url = self.website
		crawler = Crawler(url)
		crawler.crawl_all_links()
		#print('Results: ', crawler.results)
		self.messages = crawler.results

class SatelitApp(App):
	def build(self):
		root = Root()
		return root
		
		def on_stop(self): # this isn't working'
			root.ssh.close()
			print('Exiting')
		
if __name__ == '__main__':
	SatelitApp().run()
