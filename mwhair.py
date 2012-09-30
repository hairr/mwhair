#################################################################################
## MWHair - Mediawiki wrapper
## Description - This is a mediawiki client written by Hairr <hairrazerrr@gmail.com>
## It was orignally created to be used at http://runescape.wikia.com/
##
## This library is free software; you can redistribute it and/or modify it under
## the terms of the GNU Lesser General Public License as published by the Free
## Software Foundation; either version 2.1 of the License, or (at your option)
## any later version.
##
## This library is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
## FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
## details.
##
## You should have received a copy of the GNU General Public License along with
## this program.  If not, see <http://www.gnu.org/licenses/>.


import urllib2
import urllib
import json
import sys
from cookielib import CookieJar

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
logged_in = False

def login(username, password):
	"""
	@description: Used to login to the mediawiki through the API
	@use:
	import mwhair

	mwhair.login(username, password)
	"""
	login_data = { 
	'action'    :  'login',
	'lgname'    : username, 
	"lgpassword": password, 
	'format'    : 'json'
	}
	data = urllib.urlencode(login_data)
	response = opener.open("http://runescape.wikia.com/api.php", data)
	content = json.load(response)
	login_data['lgtoken'] = content['login']['token']
	data = urllib.urlencode(login_data)
	response = opener.open('http://runescape.wikia.com/api.php', data)
	content = json.load(response)
	if content['login']['result'] == 'Success':
		print 'Now logged in as %s' % content['login']['lgusername']
		logged_in = True
		edittokens()
	elif content ['login']['result'] == 'NeedToken':
		print 'Error occured while trying to log in...'
		sys.exit(1)
	elif content ['login']['result'] == 'WrongPass':
		print 'Incorrect password.'
		sys.exit(1)
	else:
		print 'Error occured.'
		sys.exit(1)

def logout():
	"""
	@description: Used to logout of the wiki through the API
	@use:
	import mwhair

	mwhair.logout()
	"""
	logout_data = {
	'action':'logout',
	'format':'json'
	}
	data = urllib.urlencode(logout_data)
	response = opener.open('http://runescape.wikia.com/api.php', data)
	content = json.load(response)
	print "Successfully logged out"

def edittokens():
	"""
	@description: Used to gather tokens to edit, delete, protect, move, block, unblock, email, and import
	@use: This shouldn't be used in a seperate script, the information is gathered on login
	"""
	edit_token_data = {
	'action':'query',
	'prop':'info',
	'titles':'Main Page',
	'intoken':'edit|delete|protect|move|block|unblock|email|import',
	'format':'json'
	}
	data = urllib.urlencode(edit_token_data)
	response = opener.open('http://runescape.wikia.com/api.php', data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	try:
		warnings = content['warnings']['info']['*']
	except:
		warnings = None
	if warnings != None:
		if 'edit' in warnings:
			print 'No edit token: Quitting....'
			sys.exit(1)
		else:
			edit_token = thes['edittoken']

		if 'delete' in warnings:
			delete_token = None
		else:
			delete_token = thes['deletetoken']

		if 'protect' in warnings:
			protect_token = None
		else:
			protect_token = thes['protecttoken']

		if 'move' in warnings:
			move_token = None
		else:
			move_token = thes['movetoken']

		if 'block' in warnings:
			block_token = None
		else:
			block_token = thes['blocktoken']

		if 'unblock' in warnings:
			unblock_token = None
		else:
			unblock_token = thes['unblocktoken']

		if 'email' in warnings:
			email_token = None
		else:
			email_token = thes['emailtoken']

		if 'import' in warnings:
			import_token = None
		else:
			import_token = thes['importtoken']
	else:
		edit_token = thes['edittoken']
		delete_token = thes['deletetoken']
		protect_token = thes['protecttoken']
		move_token = thes['movetoken']
		block_token = thes['blocktoken']
		unblock_token = thes['unblocktoken']
		email_token = thes['emailtoken']
		import_token = thes['importtoken']