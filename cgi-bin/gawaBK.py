#!/usr/local/Python-2.7.3/bin/python
import sys, MySQLdb, cgi, cgitb, re, random, string, datetime, os.path, json
cgitb.enable()

####  THIS IS OUR FINAL PROJECT CODE ####
#### LAST MODIFIED ON April 28, 2013 4:10:30 AM EDT ####



### DATABASE CONNECTION CODE ###

def connect_db(username,pswd):
	#connect to database
	connection = MySQLdb.connect(host="localhost", db="gawa", user=username, passwd=pswd)
	#get cursor
	cursor = connection.cursor()
	return cursor, connection

def close_db(cursor, connection):
	#close cursor and connection
	cursor.close()
	connection.close()


### THESE DEFINITIONS ARE FROM GawaImage.py FROM AMAUCHE E. EMAILED ON 4/24/2013 17:35 ###
### SCRIPT IS IN RAW FORM, NO EDITING PERFORMED ###

# def createAnimatedGIF(strArr):
# 	if (not isinstance(strArr,list)):
# 		print "Input is not an array"
# 		return None
# 	if len(strArr)<1:
# 		print "Array cannot be empty"
# 		return []
# 
# 	from PIL import Image
# 	from images2gif import writeGif
# 	import os, datetime
# 
# 	resultArr = convertToGIF(strArr,700,fullPath=False)
# 
# 	images = [Image.open(fn) for fn in resultArr]
# 	tempfolder = os.path.split(resultArr[0])[0]
# 	epochtime = str(datetime.datetime.now().strftime('%s'))
# 	dstPath = os.path.join(tempfolder,"my_gif"+epochtime+".GIF")
# 	output = writeGif(dstPath,images, duration=0.2)
# 
# 	if(os.path.exists(dstPath)):
# 		return [getURLPath(dstPath)]
# 	else:
# 		print "I failed to create animated GIF "+filename
# 		return None
# 
# 
# def convertToGIF(strArr,size=-1,fullPath=True):
# 	if (not isinstance(strArr,list)):
# 		print "Input is not an array"
# 		return None
# 	if len(strArr)<1:
# 		print "Array cannot be empty"
# 		return []
# 
# 	import os, tempfile, datetime,shutil
# 	from subprocess import call
# 
# 	epochtime = str(datetime.datetime.now().strftime('%s'))
# 	mystuff = '/www/html/students_13/amauche'
# 	tempfolder = os.path.join(mystuff,"images",epochtime)
# 
# 	if not os.path.exists(tempfolder):os.makedirs(tempfolder)
# 	resultArr = []
# 
# 	#This section removes all th directories created that are older than 6 minutes.
# 		for top, dirs, files in os.walk(os.path.dirname(tempfolder)):
# 			for subd in dirs:
# 				if subd.isdigit():
# 					tstamp = int(subd)
# 					if int(datetime.datetime.now().strftime('%s'))-tstamp>360:
# 						try :
# 							shutil.rmtree(os.path.join(top,subd))
# 						except :
# 							pass
# 
# 	for fiPath in strArr:
# 		if fiPath.endswith('.tif'):
# 				justName = os.path.split(fiPath)[-1].split('.')[0]
# 				dstPath = os.path.join(tempfolder,justName + ".gif")
# 				if os.path.exists(dstPath):os.remove(dstPath)
# 				if(size is None or not isinstance(size,int) or size < 0):
# 					output = call(["/usr/bin/convert",fiPath, dstPath])
# 				else:
# 					output = call(["/usr/bin/convert","-resize",str(size)+"x"+str(size),fiPath, dstPath])
# 
# 				if(os.path.exists(dstPath)):
# 					if(fullPath): dstPath = getURLPath(dstPath)
# 						resultArr.append(dstPath)
# 
# 	return resultArr
# 
# 
# def convertToThumb(strArr,fullPath=True):
# 	return convertToGIF(strArr,size=200,fullPath=fullPath)
# 
# 
# def zipImages(sourceFolder):
# 	import os,datetime,zipfile
# 		
# 	destination='/www/html/students_13/amauche'
# 	epochtime = str(datetime.datetime.now().strftime('%s'))
# 		
# 	dfolder = os.path.join(destination,'zipfiles')
# 	if not os.path.exists(dfolder):os.makedirs(dfolder)
# 	dfile = os.path.join(dfolder,epochtime+".zip")
# 		
# 	zf = zipfile.ZipFile(dfile, "w")
# 	containFolder = os.path.abspath(sourceFolder)
# 	for dirname, subdirs, files in os.walk(containFolder):
# 		for filename in files:
# 			filepath = os.path.abspath(os.path.join(dirname, filename))
# 			zf.write(filepath, filename)
# 	zf.close()
# 
# 	#This section removes all the files created that are older than 2 minutes.
# 	for top, dirs, files in os.walk(dfolder):
# 		for file in files:
# 			fname = file.split('.')[0]
# 			if fname.isdigit():
# 				tstamp = int(fname)
# 				if int(datetime.datetime.now().strftime('%s'))-tstamp>120:
# 					try :
# 						os.remove(os.path.join(top,file))
# 					except :
# 						pass
# 	return getURLPath(dfile)
# 
# 
# def getURLPath(path):
# 	str1 = path.split('html/')[-1]
# 	httpAdr = "http://bioed.bu.edu/"
# 	dstPath = httpAdr+str1
# 	return dstPath


### COOKIE/SESSION CODE FROM AMAUCHE GOES HERE ###




### BROWSE FUNCTION CODE FROM WILL ### 
### TAKEN FROM HIS EMAILED CODE ON APRIL 25 2013 at 17:29 ###
def get_column(results, index):
	col = []
	for result in results:
		col.append(result[index])
	return col
		
def print_browse_by_form():
	print '<form id = "form_browse_by">'	
	print '<label for = "browse_by">browse by:</label>'
	print '<select name = "browse_by" id = "browse_by" class = "drawOptionsOnChange">'
	print '<option value = "none">Select Result Type</option>'
	print '<option value = "Animal">Animal</option>'
	print '<option value = "Experiment">Experiment</option>'
	print '<option value = "Image">Image</option>'
	print '</select>'
	print '</form>'
	# print container for AJAXed options
	print '<div id = options-wrapper><div>'

def print_form(cols, results, browse_by):
	print '<form id = "form_options" class = "ajax-destroyable-options">'
	print '<input type = "hidden" name = "browse" value = "' + browse_by + '">'
	for i in range(len(cols)):
		colHead = str(cols[i][0])
		colOptions = set(get_column(results, i))
		print '<label for = "' + colHead + '">' + colHead + ':</label>'
		print '<select name = "' + colHead  + '" id = "' + colHead + '" class = "drawTableOnChange">'
		print '<option value = "">any</option>'
		while (len(colOptions) != 0):
			option = str(colOptions.pop())
			print '<option value = "' + option + '">' + option + '</option>'
		print '</select><br>' #REMOVE <BR> TAG AFTER CSS IS APPLIED!	
	print '</form>'

def print_table(cols, results, browse_by):
	print '''
	<div id = "results-wrapper" class = "ajax-destroyable-options">
        	<table id = "results">
			<tr>'''
	for col in cols:
		print '<th class = "' + str(col[0]) + '">' + str(col[0]) + '</th>'
	print '</tr>'
	
	# table below this point will be redrawn with ajax when user modifies parameters
	for j in range(len(results)):
		getString = '?to' + browse_by + 'Page=true&'  #built GET key/val pairs to place into the anchor tag
		getString += str(cols[0][0]) + '=' + str(results[0][0])	
		print '<tr class = "ajax-destroyable">'
		for i in range(len(cols)):
			print '<td class = "' + str(cols[i][0]) + '"><a href = "browse.py' + getString + '">' + str(results[j][i]) + '</a></td>'
		print '</tr>'

	print '</table>'
	print '<div>'

# prints the checkboxes that control the visible result fields
def print_display_options(cols, resultType):
	print '<form id = "display_options" class = "ajax-destroyable-options">'
	for col in cols:
		print '<input type = "checkbox" class = "checkbox" checked = "true" id = "' + col[0] + '" name = "show_field_' + col[0] + '" value = "on">'
		print '<label for = "' + col[0] + '">' + col[0] + '</label>'
	print '</form>'

def query_gawa(query):
	cursor.execute(query)
	results = cursor.fetchall()
	return results




### HTML BUILDING CODE ###
### USE ABSOLUTE PATHS to CSS & IMAGES in HTML FOLDER ###
### /students_13/gawa/images ###
### /students_13/gawa/style.css ###

def print_HTML_head():
	print "Content-type: text/html\n"
	print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml-strict.dtd\">"
	print "<html xmlns=\"http://www.w3.org/1999/html\" lang=\"en\" xml:lang=\"en\">"
	print "<head>"
	print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=ISO-8859-1\" />"
	print "<title>GAWA | Gerbil Aural World Access</title>"
	print "<link rel=\"stylesheet\" type=\"text/css\" href=\"/students_13/gawa/style_new.css\" />"
	print "<link href='http://fonts.googleapis.com/css?family=Roboto+Condensed' rel='stylesheet' type='text/css'>"
	print "<link href='http://fonts.googleapis.com/css?family=Quicksand' rel='stylesheet' type='text/css'>"
	print "<script src=\"http://code.jquery.com/jquery-1.9.1.min.js\"></script>"
	print "<script src=\"/students_13/gawa/browse.js\"></script>"
	print "</head>"
	print "<body>"
	
def print_HTML_header_login_logo(loginstatus=0,user="",session_key=""):
	print "<div id=\"header\">"
	print "<div id=\"login\">"
	if loginstatus == 0:
		print "<form name=\"login\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\">Sign in: <input type=\"text\" name=\"username\" placeholder=\"username\"><input type=\"text\" name=\"password\" placeholder=\"password\"><input type=\"image\" name=\"submit\" id=\"submit\" src=\"/students_13/gawa/images/go.png\"></form>"
	elif loginstatus == 1:
		print "<form name=\"login\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\">Sign in: <input type=\"text\" name=\"username\" placeholder=\"username\"><input type=\"text\" name=\"password\" placeholder=\"password\"><input type=\"image\" name=\"submit\" id=\"submit\" src=\"/students_13/gawa/images/go.png\"></form>"
		print "<p class=\"error\">Nice try, wrong credentials.</p>"
	elif loginstatus == 2:
		print "<p>Welcome %s.</p>" %(user)
		print "<form name=\"login\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\"> <input type='hidden' NAME='session_key' VALUE='%s'>Logout: <input type=\"image\" name=\"submit\" id=\"submit\" src=\"/students_13/gawa/images/go.png\"></form>" %s(session_key)
	print "</div>  <!--HEADER LOGIN END-->"
	print "<div id=\"logo\"><img src=\"/students_13/gawa/images/gawa-logo2s.png\" width=\"208\" height=\"67\" alt=\"logo\" /></div>"
	print "<!--HEADER LOGO END-->"

def print_HTML_navigation(current_page):
	print "<div id=\"navigation\">"
	home_current = browse_current = update_current = help_current = about_current = ""
	if current_page == "home":
		home_current = "id=\"current\""
	elif current_page == "browse":
		browse_current = "id=\"current\""
	elif current_page == "update":
		update_current = "id=\"current\""
	elif current_page == "help":
		help_current = "id=\"current\""
	elif current_page == "about":
		about_current = "id=\"current\""
	print "<div class=\"navbox\"><a %s href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=home\"><img src=\"/students_13/gawa/images/home.png\" /><br>HOME</a></div>" %(home_current)
	print "<div class=\"navbox\"><a %s href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=browse\"><img src=\"/students_13/gawa/images/search.png\" /><br>BROWSE</a></div>" %(browse_current)
	print "<div class=\"navbox\"><a %s href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=update\"><img src=\"/students_13/gawa/images/edit.png\" /><br>UPDATE</a></div>" %(update_current)
	print "<div class=\"navbox\"><a %s href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help\"><img src=\"/students_13/gawa/images/help.png\" /><br>HELP</a></div>" %(help_current)
	print "<div class=\"navbox\"><a %s href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=about\"><img src=\"/students_13/gawa/images/about.png\" /><br>ABOUT</a></div>" %(about_current)
	print "</div> <!--HEADER NAVIGATION END-->"
	print "</div> <!--HEADER END-->"
	
def print_HTML_content_pre():
	print "<!--WRAPPER MAIN HERE-->"
	print "<div id=\"content_wrapper\">"
	print "<!--SIDEBAR (OPTIONAL) HERE-->"
	print "<div id=\"sidebar_outer\">"
	print "<div id=\"sidebar_inner\">"

def print_HTML_content_mid():
	print "</div> </div><!--SIDEBAR END-->"
	print "<!--MAIN CONTENT-->"
	print "<div id=\"maincontent_outer\">"
	print "<div id=\"maincontent_inner\">"

def print_HTML_content_post():
	print "</div> </div><!--MAIN CONTENT END-->"
	print "</div> <!--WRAPPER MAIN END-->"
	print "<div style=\"clear:both;\"></div>"
	
def print_HTML_content_single_pre():
	print "<!--WRAPPER MAIN HERE-->"
	print "<div id=\"content_wrapper\">"
	print "<div id=\"content_wrapper_inner\"> <!--INNER WRAPPER (CONDITIONAL, TO BE USED IF NO SIDEBAR)-->"

def print_HTML_content_single_post():
	print "</div> <!--INNER WRAPPER (CONDITIONAL) END-->"
	print "</div> <!--WRAPPER MAIN END-->"
	print "<div style=\"clear:both;\"></div>"

def print_HTML_tail():
	print "</body>"
	print "</html>"
	
### SESSION CODE GOES HERE ###

## code that generates the login form is under the ### HTML BUILDING CODE ### Section. ##




### QUICK QUERIES ###

def quickquery_run(qqueryid=0,param1="",param2="",param3="",param4=""):
	## which images no ROI
	if qqueryid == 1:
		query = "SELECT Image.iid FROM Image LEFT JOIN Image_has_ROI ON Image.iid = Image_has_ROI.Image_id WHERE ROI_id IS NULL;"
		query_desc = "List of images without ROIs"
	if qqueryid == 2:
		query = "SELECT * FROM Experiment;"
		query_desc = "All Experiments"
	## REMOVED QUERY 3 ###
	if qqueryid == 4:
		query = "SELECT e.eid, e.experiment_id FROM Experiment e LEFT JOIN (Image i JOIN Image_has_ROI r ON i.iid = r.Image_id) ON e.experiment_id = i.experiment_eid WHERE ROI_id IS NULL;"
		query_desc = "Experiments with no ROIs associated"
	if qqueryid == 5:
		query = "SELECT e.eid, e.experiment_id, e.ear, e.animal_id FROM Experiment e WHERE e.tonotopicLocation IS NULL;"
		query_desc = "Experiments without Tonotopic Location Defined"

	#get and return results of query
	cursor.execute(query)
	results = cursor.fetchall()

	#print query description
	print "<h2>%s</h2>" %(query_desc)

	# check to see if results exist
	if not results:
			print "<h3 class=\"error\">Sorry, your query did not return any results.</h3>"
	else:
		# print the results table	
		description = cursor.description
		print "<table><thead><tr>"
		for item in description:
			print "<th>"+item[0]+"</th>"
		print "</tr></thead>"
		for item in results:
			print "<tr>"
			for i in range(len(item)):
				print "<td>",item[i],"</td>"
			print "</tr>"
		print "</table>"

def print_HTML_quickquery():
	print """<div id='searchbox'>
	<div class='quick-search'>
	<h1>QUICK SEARCH</h1>
	<form name="quicksearch" action="http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py" method="POST"> 
	<select name='quicksearchoption'>
	<option value='cat-1'>Category 1</option>
	<option value='cat-2'>Category 2</option>
	<option value='cat-3'>Category 3</option>
	</selct>
	<input name="quicksearchkeyword" value="keyword" type="text" />
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	</div> <!--END QUICK-SEARCH-->
	<div class='fast-query'>
	<h1>QUICK QUERIES</h1>
	<form name=\"quickquery\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\">
	<select name='quickqueryoption'>
	<option value='q1'>Images without ROI</option>
	<option value='q4'>Experiments without ROI</option>	
	<option value='q2'>All Experiments</option>
	<option value='q5'>Experiments without a Tonotopic Location</option>
	</select>
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	</div> <!--END QUICK-QUERIES-->
	<div class='semi-quick-query'>
	<h1>SEMI QUICK QUERIES</h1>
	<form name="semiquickquery" action="http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py" method="POST">
    <label>Find all images whose Tonotopic Map has: </label>
	<select name='tonotopic map'>
	<option value='t1'>TCH</option>
	<option value='t2'>CDIH</option>	
	<option value='t3'>SDKSD</option>
	<option value='t4'>CHCs</option>
	</select>
    <label>And whose keywords contain: </label>
    <input name="keyword" value="keyword" type="text" />
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	</div> <!--END SEMI-QUICK-QUERY-->
	</div> <!--END SEARCHBOX - NOT USED FOR CSS-->"""



### RUNNING PROGRAM CODE ###


#print beginning html
print_HTML_head()
print_HTML_header_login_logo()  #loginstatus=0,user="",session_key=""

#connect to DB and get cursor
cursor, connection = connect_db("jiwani","24horse!!")

# first get the form
form = cgi.FieldStorage()

# print navigation
if "page" in form:
	current_page = form["page"].value
else:
	current_page = "home"
print_HTML_navigation(current_page)

#check if the form has ever been used before
if current_page == "home":
	print_HTML_content_pre()
	print_HTML_quickquery()
	print_HTML_content_mid()
	
	if "quickqueryoption" in form:
		qquery = form["quickqueryoption"].value
		if qquery == "q1":
			quickquery_run(qqueryid=1)
		if qquery == "q2":
			quickquery_run(qqueryid=2)
		if qquery == "q3":
			quickquery_run(qqueryid=3)
		if qquery == "q4":
			quickquery_run(qqueryid=4)
		if qquery == "q5":
			quickquery_run(qqueryid=5)

	print_HTML_content_post()

# if current_page == "browse":
# 	### FOLLOWING CODE FROM WILL'S BROWSE.PY FILE ###
# 	
# 	if form.has_key('browse_by'): # then the user has just set a browse result type. print the relevent filter options
# 		resultType = form['browse_by'].value
# 		if resultType == 'none': 
# 			sys.exit()
# 		if resultType == 'Image': # must group by on image queries to get image sets
# 			query = '''
# 				SELECT *, COUNT(*)
# 				FROM Image 
# 				GROUP BY experiment_eid, focalPlaneLevel, daqFreq; 
# 				'''
# 
# 		else: #resultType = Animal, Experiment, or ROI 
# 			query = '''
# 			SELECT * 
# 			FROM %s; 
# 			''' % form['browse_by'].value # Animal, Experiment, or Image
# 		
# 		results = query_gawa(query)
# 
# 		query = '''
# 		SHOW COLUMNS FROM %s;
# 		''' % form['browse_by'].value # Animal, Experiment, or Image
# 	
# 			
# 		columnNames = query_gawa(query)
# 		print_display_options(columnNames,resultType);	
# 		print_form(columnNames, results, resultType);
# 		print_table(columnNames, results, resultType);
# 		
# 	 	
# 	else: # user just filtered some results
# 		resultType = form['browse'].value
# 		displayFields = []
#                 for key in form:
#                         if 'show_field' in key:
#                                 displayFields.append(key)
# 
# 		query = '''
# 		SHOW COLUMNS FROM {0};
# 		'''.format(resultType) # Animal, Experiment, or Image
# 	
# 		cols = query_gawa(query)
# 		selectFields = ''
# 		for col in cols:
# 			selectFields += ',' + str(col[0])
# 		selectFields = selectFields[1:]
# 			
# 		if len(form) == 1 + len(displayFields): # then the only field is the hidden field, and all parameters have been set to 'any'		
# 			if resultType == 'Image': 
# 				query = '''
# 				SELECT *, COUNT(*) 
# 				FROM Image
# 				GROUP BY experiment_eid, focalPlaneLevel, daqFreq; 
# 				'''
# 			else: #resultType = Animal, Experiment, or ROI  	
# 
# 				query = '''
# 				SELECT * 
# 				FROM {0}; 
# 				'''.format(resultType)
# 		
# 		else:
# 			queryAttributes = ''
# 			for key in form: 
# 				if key != 'browse' and 'show_field' not in key:
# 					queryAttributes += 'and ' + key + ' = "' + form[key].value + '"'
# 			queryAttributes = queryAttributes[3:] #strip off first 'and'	
# 			if resultType == 'Image':
# 				
# 				query = '''
# 				SELECT *, COUNT(*)
# 				FROM Image
# 				WHERE {0}
# 				GROUP BY experiment_eid, focalPlaneLevel,  daqFreq;
# 				'''.format(queryAttributes)
# 
# 			else: #resultType = Animal, Experiment, or ROI  	
# 				query = '''
# 				SELECT * 
# 				FROM {0}
# 				WHERE {1} ; 
# 				'''.format(resultType, queryAttributes) 
# 			
# 		results = query_gawa(query)
# 
# 		
# 		if results: #query returned > 0 results
# 			
# 			resultType = form['browse'].value	
# 			output = ''	
# 			for result in results:
# 				getString = '?to' + resultType + 'Page=true&'  #build URL string with result type and ID
# 				if resultType == 'Animal':
# 					getString += 'aid='
# 				elif resultType == 'Experiment':
# 					getString += 'eid='
# 				else: # resultType == 'Image'
# 					getString += 'iid=' 
# 				getString += str(result[0])
# 				output += '<tr class = "ajax-destroyable">'
# 				count = 0
# 				print '<p>'+ str(cols) + '</p>'
# 				print '<p>' + str(result) + '</p>'	
# 	
# 				for i in range(len(result)):# MAYBE - 1???ASDformADFASFASDF	
# 					output += '<td class = ' + str(cols[i][0]) + '><a href = "' + getString + '">' + str(result[i]) + '</td>'
# 				output += '</tr>'
# 			print output
# 		else: #query returned nothing
# 			print '<p class = "ajax-destroyable">I\'m sorry, there are no items with those attributes.</p>'
# 
# 	else:
# 	# then it is the user's first time on the page. 
# 	# run initial query and display all results
# 	# also populate the select menues with relevant choices.
# 
# 		print_header()	
# 		print_browse_by_form()


#print ending html
print_HTML_content_post()
print_HTML_tail()

#close connection to DB
close_db(cursor, connection)
