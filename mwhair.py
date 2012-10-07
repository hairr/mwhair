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

def site(site):
	"""
	@description: Sets the wiki's api
	@use:
	import mwhair

	mwhair.wiki('http://foo.com/api.php')
	@other: You must specifiy the url of the api with the http protocol and without the www
	"""
	global wiki
	wiki = site

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
	response = opener.open(wiki, data)
	content = json.load(response)
	login_data['lgtoken'] = content['login']['token']
	data = urllib.urlencode(login_data)
	response = opener.open(wiki, data)
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
	response = opener.open(wiki, data)
	content = json.load(response)
	print "Successfully logged out"

def edittokens():
	"""
	@description: Used to gather tokens to edit, delete, protect, move, block, unblock, email, and import
	@use: This shouldn't be used in a seperate script, the information is gathered on login and used throughout mwhair
	"""
	edit_token_data = {
	'action':'query',
	'prop':'info',
	'titles':'Main Page',
	'intoken':'edit|delete|protect|move|block|unblock|email|import',
	'format':'json'
	}
	data = urllib.urlencode(edit_token_data)
	response = opener.open(wiki, data)
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
			global edit_token
			edit_token = thes['edittoken']

		if 'delete' in warnings:
			global delete_token
			delete_token = None
		else:
			delete_token = thes['deletetoken']

		if 'protect' in warnings:
			global protect_token
			protect_token = None
		else:
			protect_token = thes['protecttoken']

		if 'move' in warnings:
			global move_token
			move_token = None
		else:
			move_token = thes['movetoken']

		if 'block' in warnings:
			global block_token
			block_token = None
		else:
			block_token = thes['blocktoken']

		if 'unblock' in warnings:
			global unblock_token
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

def purge(title):
	"""
	@description: Purges the specified page
	@use:
	import mwhair

	mwhair.purge('foo')
	"""
	purge_data = {
	'action':'purge',
	'titles':title,
	'format':'json'
	}
	data = urllib.urlencode(purge_data)
	response = opener.open(wiki,data)
	content = json.load(response)

def edit(title, section=None):
	"""
	@description: Gathers information about a specified page
	@use:import mwhair

	foo = mwhair.edit('bar')
	@other: This then makes the variable foo the contents of bar
	"""
	read_page_data = {
	'action':'query',
	'prop':'revisions',
	'titles':title,
	'rvprop':'timestamp|content',
	'format':'json'
	}
	if section:
		read_page_data['rvsection'] = section
	data = urllib.urlencode(read_page_data)
	response = opener.open(wiki, data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	try:
		wikipage = thes['revisions'][0]['*']
		return wikipage
	except KeyError:
		wikipage = ''
		return wikipage


def save(title, text='',summary='',minor=False,bot=True,section=False):
	"""
	@description: Saves the contents of the page
	@use:
	import mwhair

	mwhair.save('foo')
	@other: text needs to be specified, if not, the page will only be purged
	to create a non-bot edit, specifiy bot=False, otherwise, it'll be marked as a bot edit
	"""
	save_data = {
	'action':'edit',
	'title':title,
	'text':text.encode('utf-8'),
	'summary':summary,
	'minor':minor,
	'token':edit_token,
	'format':'json'
	}
	if bot is False:
		pass
	else:
		save_data['bot'] = 'True'
	if not text:
		save_data['text'] = purge(title) # This will make the page purge
	if section != False:
		save_data['section'] = section
	if text:
		data = urllib.urlencode(save_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content

def move(fromp, to, movesubpages=True, movetalk=True,reason='',noredirect=False):
	"""
	@description: Moves one page to another
	@use:
	import mwhair

	mwhair.move('Foo','Bar')
	"""
	move_data = {
	'action':'move',
	'from':fromp,
	'to':to,
	'reason':reason,
	'token':move_token,
	'format':'json'
	}
	if movesubpages == True:
		move_data['movesubpages'] = True

	if movetalk == True:
		move_data['movetalk'] = True

	if noredirect == True:
		move_data['noredirect'] = True
	if move_token is not None:
		data = urllib.urlencode(move_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content
	else:
		print 'You do not have permission to move.'

def upload(filename, url, comment=''):
	"""
	@description: Uploads a file from another url
	@use:
	import mwhair

	mwhair.upload('File.png','http://foo.com/bar.png')
	"""
	upload_data = {
	'action':'upload',
	'filename':filename,
	'url':url,
	'comment':comment,
	'token':edit_token,
	'format':'json'
	}
	data = urllib.urlencode(upload_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	return content

def delete(title, reason=None):
	"""
	@description: Deletes a specified page
	@use:
	import mwhair

	mwhair.delete('Foo')
	"""
	delete_data = {
	'action':'delete',
	'title':title,
	'token':delete_token,
	'format':'json'
	}
	if reason != None:
		delete_data['reason'] = reason
	if delete_token is not None:
		data = urllib.urlencode(delete_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content
	else:
		print 'You do not have permission to delete.'

def protect(title,edit="all",move="all",expiry="infinite",reason=None):
	"""
	@description: Protects the specified page
	@use:
	import mwhair

	mwhair.protect('foo')
	"""
	protect_data = {
	'action':'protect',
	'title':title,
	'protections':'edit=' + edit + '|move=' + move,
	'expiry':expiry,
	'token':protect_token,
	'format':'json'
	}
	if reason != None:
		protect_data['reason'] = reason
	if protect_token is not None:
		data = urllib.urlencode(protect_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content
	else:
		print 'You do not have permission to protect.'

def unprotect(title,edit="all",move="all",reason=None):
	unprotect_data = {
	'action':'protect',
	'title':title,
	'protections':'edit=' + edit +'|move=' + move,
	'token':protect_token,
	'format':'json'
	}
	if reason != None:
		unprotect_data['reason'] = reason
	if protect_data is not None:
		data = urllib.urlencode(unprotect_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content
	else:
		print 'You do not have permission to unprotect.'

def undo(title,summary=False):
	"""
	@description: Undo's the current revision on the page
	@use:
	import mwhair

	mwhair.undo('foo')
	@other: If no summary is specified, an automatic summary will be put instead
	"""
	undo_data = {
	'action':'edit',
	'title':title,
	'token':edit_token,
	'undo':revnumber(title),
	'format':'json'
	}
	if summary != False:
		undo_data['summary'] = summary
	data = urllib.urlencode(undo_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	return content

def block(user,expiry='infinite',reason=None,nocreate=False,
	autoblock=False,noemail=False,talkpage=True,reblock=False,watch=False):
	"""
	@description: Blocks a specified user
	@use:
	import mwhair

	mwhair.block('Foo')
	@other: nocreate will prevent account creation, autoblock will block the last used IP's and 
	any sussequent IP addresses, noemail will prevent the user from sending an email through the wiki,
	if talkpage is false, the user will not be able to edit their talk page, reblock will overwrite any
	existing blocks, if watch is false, you will watch the user/IP's user and talk pages
	"""
	block_data = {
	'action':'block',
	'user':user,
	'expiry':expiry,
	'token':block_token,
	'format':'json'
	}
	if reason != None:
		block_data['reason'] = reason
	if nocreate != False:
		block_data['nocreate'] = True
	if autoblock != False:
		block_data['autoblock'] = True
	if noemail != False:
		block_data['noemail'] = True
	if talkpage != True:
		block_data['notalkpage'] = True
	if reblock != False:
		block_data['reblock'] = True
	if watch != False:
		block_data['watchuser'] = True
	if block_token != None:
		data = urllib.urlencode(block_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content
	else:
		print 'You do not have permission to block.'

def unblock(user,reason=None):
	"""
	@description: Unblocks a specified user
	@use:
	import mwhair

	mwhair.unblock('Foo')
	"""
	unblock_data = {
	'action':'unblock',
	'user':user,
	'token':unblock_token,
	'format':'json'
	}
	if reason != None:
		unblock_data['reason'] = reason
	if unblock_token != None:
		data = urllib.urlencode(unblock_data)
		response = opener.open(wiki,data)
		content = json.load(response)
		return content
	else:
		print 'You do not have permission to unblock.'

def recentchanges(bot=False,limit=20):
	"""
	@description: Gets the last 20 pages edited on the recent changes
	@use:
	import mwhair

	foo = mwhair.recentchanges()
	for pages in foo:
		print page ## This is an example of how to show the pages
		... tasks being performed ...
	"""
	recent_changes_data = {
	'action':'query',
	'list':'recentchanges',
	'rcprop':'user|title',
	'rclimit':limit,
	'format':'json'
	}
	if bot is False:
		recent_changes_data['rcshow'] = '!bot'
	data = urllib.urlencode(recent_changes_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['recentchanges'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def logs(letype=None,leaction=None,lelimit=50,lestart=None,leend=None):
	"""
	@description: Gets (default: 50) pages in the specified log, if none specified, it'll list all the logs
	@use:
	import mwhair

	foo = mwhair.logs()
	for pages in foo:
		print page ## This is only an example to show the pages
		... tasks being performed ...
	@other: To specify a log, letype="logtype". leaction will override letype.
	"""
	log_events_data = {
	'action':'query',
	'list':'logevents',
	'lelimit':lelimit,
	'format':'json'
	}
	if letype != None:
		log_events_data['letype'] = letype
	else:
		pass

	if leaction != None:
		log_events_data['leaction'] = leaction
	else:
		pass

	if lestart != None:
		log_events_data['lestart'] = lestart
	else:
		pass

	if leend != None:
		log_events_data['leend'] = leend
	else:
		pass

	data = urllib.urlencode(log_events_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['logevents'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def backlinks(title,bllimit=10,blnamespace=None):
	"""
	@description: Gets (default: 10) pages that link to the specified title
	@use:
	import mwhair

	foo = mwhair.backlinks('bar')
	for pages in foo:
		print pages ## This is only an example to show the pages
		... tasks being performed ...
	"""
	backlink_data = {
	'action':'query',
	'list':'backlinks',
	'bltitle':title,
	'bllimit':bllimit,
	'format':'json'
	}
	if blnamespace != None:
		backlink_data['blnamespace'] = blnamespace
	else:
		pass
	data = urllib.urlencode(backlink_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['backlinks'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def imageusage(title,iulimit=10,iunamespace=None):
	"""
	@description: Gets (default: 10) pages that use the specified image
	@use:
	import mwhair

	foo = mwhair.imageusage('File:Bar.png')
	for pages in foo:
		print pages ## This is only an example to show the pages
		... tasks being performed ...
	"""
	imageusage_data = {
	'action':'query',
	'list':'imageusage',
	'iutitle':title,
	'iulimit':iulimit,
	'format':'json'
	}
	if iunamespace != None:
		imageusage_data['iunamespace'] = iunamespace
	data = urllib.urlencode(imageusage_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['imageusage'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def category(title,cmlimit=10,cmnamespace=None):
	"""
	@description: Gets (default: 10) pages that are used in the specified category
	@use:
	import mwhair

	foo = mwhair.category('Category:Bar')
	for pages in foo:
		print pages ## This is only an example to show the pages
		... tasks being performed ...
	"""
	category_data = {
	'action':'query',
	'list':'categorymembers',
	'cmtitle':title,
	'cmlimit':cmlimit,
	'format':'json'
	}
	if cmnamespace != None:
		category_data['cmnamespace'] = cmdnamespace
	data = urllib.urlencode(category_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['categorymembers'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def template(title,eilimit=10,einamespace=None):
	"""
	@description: Gets (default: 10) pages that use the specified template
	@use:
	import mwhair

	foo = mwhair.template('Template:Bar')
	for pages in foo:
		print pages ## This is only an example to show the pages
		... tasks being performed ...
	"""
	template_data = {
	'action':'query',
	'list':'embeddedin',
	'eititle':title,
	'eilimit':eilimit,
	'format':'json'
	}
	if einamespace != None:
		template_data['einamespace'] = einamespace
	data = urllib.urlencode(template_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['embeddedin'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def usercontribs(title,uclimit=10,ucnamespace=None):
	"""
	@description: Gets (default: 10) pages last edited by the specified user
	@use:
	import mwhair

	foo = mwhair.usercontribs('Bar')
	for pages in foo:
		print pages ## This is only an example to show the pages
		... tasks being performed ...
	"""
	user_contrib_data = {
	'action':'query',
	'list':'usercontribs',
	'ucuser':title,
	'uclimit':uclimit,
	'format':'json'
	}
	if ucnamespace != None:
		user_contrib_data['ucnamespace'] = ucnamespace
	data = urllib.urlencode(user_contrib_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['usercontribs'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def prefix(title,aplimit=10,apprlevel=None,apnamespace=None):
	"""
	@description: Gets (default: 10) pages that begin with the specified title
	@use:
	import mwhair

	foo = mwhair.prefix('bar')
	for pages in foo:
		print pages ## This is only an example to show the pages
		... tasks being performed ...
	@other: If this being done in another namespace (Talk, User, etc..) the title input
	would be the name of the page without the namespace specified (ex. User:Foo would only be Foo)
	with the appropriate namespace number in apnamespace. Apprlevel is the protection level, 
	default None|Semi|Full
	"""
	prefix_data = {
	'action':'query',
	'list':'allpages',
	'apprefix':title,
	'aplimit':aplimit,
	'format':'json'
	}

	if apprlevel != None:
		prefix_data['apprlevel'] = apprlevel
	if apnamespace != None:
		prefix_data['apnamespace'] = apnamespace
	data = urllib.urlencode(prefix_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	pages = tuple(content['query']['allpages'])
	for title in pages:
		returnlist = [title['title'] for title in pages]
		return returnlist

def userrights(title):
	"""
	@description: Gets the userrights for the specified user
	@use:
	import mwhair

	foo = mwhair.userrights('Bar')
	for rights in foo:
		print rights ## This is only an example to show the rights
		... tasks being performed ...
	"""
	user_right_data = {
	'action':'query',
	'list':'users',
	'ususers':title,
	'usprop':'groups',
	'format':'json'
	}

	data = urllib.urlencode(user_right_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	rights = tuple(content['query']['users'][0]['groups'])
	for group in rights:
		returnlist = [group for group in rights]
		return returnlist

def pageid(title):
	"""
	@description: Get's the page id for the specified page
	@use: NOTICE: This isn't necessarily supposed to be used for another script
	import mwhair

	pageid = mwhair.pageid('foo')
	"""
	pageid_data = {
	'action':'query',
	'prop':'revisions',
	'titles':title,
	'format':'json'
	}
	data = urllib.urlencode(pageid_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	pageid = thes['pageid']
	return pageid

def revnumber(title):
	"""
	@description: Get's the current revision number for the specified page
	@use: NOTICE: This isn't necessarily supposed to be used for another script
	import mwhair

	revnumber = mwhair.revnumber('foo')
	"""
	revnumber_data = {
	'action':'query',
	'prop':'revisions',
	'titles':title,
	'format':'json'
	}
	data = urllib.urlencode(revnumber_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	revnumber = thes['revisions'][0]['revid']
	return revnumber

def revuser(title):
	"""
	@description: Gets the last user to edit the specified pages
	@use:
	import mwhair

	revuser = mwhair.revuser('Foo')
	"""
	revuser_data = {
	'action':'query',
	'prop':'revisions',
	'titles':title,
	'rvprop':'user',
	'format':'json'
	}
	data = urllib.urlencode(revuser_data)
	response = opener.open(wiki,data)
	content = json.load(response)
	s = content['query']['pages']
	thes = tuple(s.values())[0]
	revuser = thes['revisions'][0]['user']
	return revuser