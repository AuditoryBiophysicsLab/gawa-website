#!/usr/local/Python-2.7.3/bin/python
import cgi, string, cgitb
from hashlib import sha224
cgitb.enable()

def sessions_file():
	return 'sessions.txt'
	
def psswd_file():
	return 'xkcd.txt'

# Define function to test if the user exists.
def test_usr(id):
        output = False
        for line in passwd_file.readlines():
                line = line.strip()
                combo = line.split(":")
                if (id==combo[0]):
                        output = True
                        break
        passwd_file.close()
        return output

# Define function to test the password.
def test_passwd(id, passwd):
        inc_pass = sha224(passwd).digest()
        passwd_file = open(psswd_file(), 'r')
        output = "failed"
        for line in passwd_file.readlines():
                line = line.strip()
                combo = line.split(":")
                if (id==combo[0] and inc_pass==combo[1]):
                        output = "passed"
                        break
        passwd_file.close()
        return output
	
# Define function to create a session.  The sessions.txt file must exists and be writable.
def create_session(id):
	import uuid,datetime
	session_file = open(sessions_file(), 'w')
	session_key = uuid.uuid4()
	session_start = datetime.datetime.now().strftime('%s') # number of seconds since epoch
	session_file.write(str(session_key)+":"+id+":"+session_start) 
	session_file.close()
	return session_key


# Define a function to return username.
def fetch_username(key):
	output = None
	session_file = open(sessions_file(), 'r')
	for line in session_file.readlines():
		if ":" in line:
			values = string.split(line, ":")
			if values[0] == str(key):
				output = values[1]
				#Should I check here to see if the session has expired?
	session_file.close()
	return output

# Define function to delete a session.
def delete_session(id):
	session_file = open(sessions_file(), 'r')
	lines = session_file.readlines()
	session_file.close()
	session_file = open(sessions_file(), 'w')
	session_file.write("")
	for line in lines:
		values = string.split(line, ":")
		if values[0] == id:
			continue
		else:
			session_file.write(line)
	session_file.close()

def create_cookie(id):
        import Cookie
        import datetime
        import os

        expiration = datetime.datetime.now() + datetime.timedelta(days=60)
        cookie = Cookie.SimpleCookie()
        cookie["gawa_session"] = str(id)
        cookie["gawa_session"]["path"] = "/"
        cookie["gawa_session"]["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")

        return cookie

def get_cookie():
        import Cookie,uuid

        output = None
        try:
                cookie = Cookie.SimpleCookie()
                cookie.load(os.environ["HTTP_COOKIE"])
                if("gawa_session" in cookie):
                        output = uuid.UUID(cookie["gawa_session"].value)
        except:
                pass
        return output



#Unchanged functions

def print_head():
	print "Content-type: text/html\n"
	print "<html>"
	print "<title>Sessions Example</title>"
	print "<body>"

def print_tail():
	print "</body>"
	print "</html>"

def generate_login_form():
	print """<form name=\"login\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\">
		Sign in: <input type=\"text\" name=\"username\" placeholder=\"username\">
		<input type=\"password\" name=\"password\" placeholder=\"password\">
		<input type=\"image\" name=\"action\" value=\"Enter\" id=\"submit\" src=\"/students_13/gawa/images/go.png\">
		</form>"""	

# Define function display_page.
def display_page(result, id, session_key = 0):
	if (result == "passed"):
		if (session_key == 0):
			session_key = create_session(id)
		print "<p>Welcome %s.</p>" %(id)
		print """<form name=\"byebye\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\">
		      <input type='hidden' NAME='session_key' VALUE='%s'>
		      Logout: <input type=\"image\" name=\"Logout\" VALUE=\"Logout\" id=\"submit\" src=\"/students_13/gawa/images/go.png\">
		      </form>""" %(session_key)
	else:
		generate_login_form()
		print "<p class=\"error\">Nice try, wrong credentials.</p>"
		
# other code removed
