# leandras_site/test/test_landing.py

import unittest
from leandras_site import app

class ProjectTests(unittest.TestCase):

	### setup and teardown ###

	# executed prior to each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['DEBUG'] = False
		self.app = app.test_client()

		self.assertEquals(app.debug, False)

	# executed after each test
	def tearDown(self):
		pass

	### Tests ###
	