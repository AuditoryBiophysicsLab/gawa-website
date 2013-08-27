#!/usr/local/Python-2.7.3/bin/python
import cgi, string, cgitb
cgitb.enable()

def sessions_file():
	return 'sessions.txt'
	
def psswd_file():
	return 'xkcd.txt'
	
# Define function to test the password.
def test_passwd(id, passwd):
	passwd_file = open(psswd_file(), 'r')
	output = "failed"
	for line in passwd_file.readlines():
		line = line.strip()
		combo = line.split(":")
		if (id==combo[0] and passwd==combo[1]):
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
	session_file = open(session_file(), 'r')
	for line in session_file.readline():
		if ":" in string:
			values = string.split(line, ":")
			if values[0] == key:
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

		print line
		if values[0] == id:
			continue
		else:
			session_file.write(line)
	session_file.close()

def create_cookie(id):
        import Cookie
        import datetime

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
	print """
		<H3>Please enter your username and password:</H3>
		<FORM METHOD='POST' ACTION='GawaSessions.py'>
		Username:<INPUT TYPE='text' NAME='username'>
		Password:<INPUT TYPE='password' NAME='password'>
		<INPUT TYPE='submit' NAME='action' VALUE='Enter'>
		</FORM>"""	
# Define function display_page.
def display_page(result, id, session_key = 0):
	if (result == "passed"):
		if (session_key == 0):
			session_key = create_session(id)
		print """<table align='right'><tr><th>Welcome %s! You are logged in with key: %s</th> 
		      <th><FORM METHOD='POST' ACTION='GawaSessions.py'>
		      <INPUT TYPE='hidden' NAME='session_key' VALUE='%s'>
		      <INPUT TYPE='submit' NAME='Logout' VALUE='Logout'>
		      </FORM></th></tr></table>
		      <br><br><br><hr>""" %(id,session_key,session_key)
		print "<p>Your content goes here.</p>" 
	else:
		print "<H3>Sorry, you entered an invalid username/password combo.</h3>"
		generate_login_form()


#  main body of code.

print_head()
form = cgi.FieldStorage()

if (form.has_key("session_key")): 
	if (form.has_key("Logout")):
		delete_session(form["session_key"].value)
		generate_login_form() 
	else:
		u_id = fetch_username(form["session_key"].value)
		display_page("passed", u_id, form["session_key"].value)
elif (form.has_key("action") and form.has_key("username") and form.has_key("password")):
	result = test_passwd(form["username"].value, form["password"].value)
	display_page(result, form["username"].value) 
else:
	generate_login_form()

print_tail()


# session