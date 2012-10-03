A MediaWiki Wrapper/Client used for Hairybot
< http://www.runescape.wikia.com/wiki/User:HairyBot >

Setting up
==========
First, change to the directory you are making your bot in. Then execute this line:
    git clone git://github.com/hairr/mwhair.git
This will then create a directory mwhair in that directory.  You can either bring the script into your current directory, or use:
    from mwhair import mwhair
at the top of your script instead.

Beginning your script
=====================
It's very easy to begin your script, simply have the first few lines like this (unless you want to import more modules of course):
    import mwhair
or if you aren't moving the script:
    from mwhair import mwhair
Then specify where the wiki's api is located, that's what it can work off of:
    mwhair.site('http://foo.com/api.php')
Now you can login:
    mwhair.login('username','password')
You are now logged in and ready to edit your wiki faster and easier.

Actions
=======
Below are all the current actions that you can perform with mwhair:

    mwhair.login('username','password')
Logs into the wiki, username and password are required

    mwhair.logout()
Logs out of the wiki, nothing is required and there is no input that can be done.  This is simply supposed to be used once you are done with a script.

    foo = mwhair.edit('Bar')
Retrieves the page contents of Bar and sets it as the variable foo.  The section can also be specified.
    
    mwhair.save('Foo') # This will purge the page Foo, as no text is specified
    mwhair.save('Foo',text='Lorem ipsum.') # This will save the page Foo, and changing all the text on the page as 'Lorem ipsum.'  
This will save the specified page.  The edit can also be saved as minor, a summary can be given, and a non-bot edit can be marked.

    mwhair.move('Foo','Bar')
This will move the page Foo to Bar, unless specified, the subpages and the talk page will be moved too.


More documentation avaliable soon...