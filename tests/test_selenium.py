#!/usr/bin/env python
#-*- coding: utf-8-*-

import unittest
from app.models import Role, User, Post
from app import db 
from app import create_app 
from selenium import webdriver
import threading
import pdb
import re
import os
import time

# class SeleniumTestCase(unittest.TestCase):
# 	client = None


# 	@classmethod
# 	def setUpClass(cls):
# 		#pdb.set_trace()
# 		try:
# 			#print(help(webdriver.Firefox))
# 			#chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
# 			#os.environ["webdriver.chrome.driver"] = chromedriver
# 			#cls.client =  webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
# 			#cls.client = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedrive.exe')
# 			#help(webdriver.Firefox)
# 			#cls.client = webdriver.Firefox()
# 			cls.client =  webdriver.Chrome("/home/zbx/python/chromedrive/chromedriver")

# 		except:
# 			pass
# 		if cls.client:
# 			cls.app = create_app('testing')
# 			cls.app_context = cls.app.app_context()
# 			cls.app_context.push()

# 			import logging
# 			logger = logging.getLogger('werkzeug')
# 			logger.setLevel('ERROR')

# 			db.create_all()
# 			Role.insert_roles()
# 			User.generate_fake(10)
# 			Post.generate_fake(20)

# 			admin_role = Role.query.filter_by(permissions=0xff).first()
# 			admin = User(email='zgg@e.com',
# 						 username='zgg', password='123',
# 						 role=admin_role, confirmed=True)
# 			db.session.add(admin)
# 			db.session.commit()

# 			threading.Thread(target=cls.app.run).start()
# 			print('threading....')
# 			#time.sleep(1)

# 	@classmethod
# 	def tearDownClass(cls):
# 		if cls.client:
# 			#pdb.set_trace()
# 			cls.client.get('http://localhost:5000/shutdown')
# 			cls.client.close()

# 			db.drop_all()
# 			db.session.remove()

# 			cls.app_context.pop()

# 	def setUp(self):
# 		#pdb.set_trace()
# 		if not self.client:
# 			self.skipTest('Web browser not available')

# 	def tearDown(self):
# 		pass

# 	def test_admin_home_page(self):
# 		pass

# 	def test_admin_home_page(self):
# 		#pdb.set_trace()
# 		self.client.get('http://localhost:5000')
# 		self.assertTrue(re.search('Stranger', self.client.page_source))
		

# 		self.client.find_element_by_link_text('Sign In').click()
# 		self.client.switch_to_window(self.client.window_handles[0])
# 		time.sleep(5)
# 		self.assertTrue('<h1>Login</h1>' in self.client.page_source)
# 		#search_windown=client.current_window_handle

# 		self.client.find_element_by_name('email').send_keys('zgg@e.com')
# 		self.client.find_element_by_name('password').send_keys('123')
# 		self.client.find_element_by_name('submit').click()
# 		time.sleep(5)

# 		#search_windown=client.current_window_handle

# 		#pdb.set_trace()
# 		self.assertTrue(re.search('zgg', self.client.page_source))

# 		self.client.find_element_by_link_text('Profile').click()
# 		time.sleep(5)
# 		self.assertTrue('<h1>zgg</h1>' in self.client.page_source)
