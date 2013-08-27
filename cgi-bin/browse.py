#!/usr/local/Python-2.7.3/bin/python

import cgi, random, os.path, cgitb, json, sys, MySQLdb
cgitb.enable() 
print "Content-type: text/html\n"

def connect_db(db,username,pswd):
        #connect to database
        connection = MySQLdb.connect (host="localhost", db=db, user=username, passwd=pswd)
        #get cursor
        cursor = connection.cursor()
        return cursor, connection

username = 'wrchapin'
password = 'pad999'
cursor, connection = connect_db("gawa",username,password)


fs = cgi.FieldStorage()

colorArray = ['2','3','4','5','6','7','8','9','a','b','c','d','e','f']
randColor = '#'
for i in range(6):
	randColor += colorArray[random.randint(0,13)]

def print_header():
	print '''
	<!DOCTYPE html>
    		<head>
			<link rel = "stylesheet" href = "/students_13/wrchapin/css/main.css">
                	<script src="http://code.jquery.com/jquery-1.9.1.min.js"></script>                	<script src="/students_13/wrchapin/js/browse.js"></script>
    	</head>
	<body style = "background-color: {0}">	
'''.format(randColor)

# takes a results object and returns all values from a single column (used to get select options)
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


def print_footer():
	print '<body>'
	print '</html>'

def query_gawa(query):
	cursor.execute(query)
	results = cursor.fetchall()
	return results
	


if fs: # then the user has just changed a browsing parameter or clicked a browse link.
	
	if fs.has_key('toAnimalPage'): # print animal info page
		
		### get animal info
		query = '''
		SELECT subjectID, species, age, weight, size
		FROM Animal 
		Where aid = {0}
		'''.format(fs['aid'].value)
		
		animalResults = query_gawa(query)

		### get experiments associated with this animal
		query = '''
		SELECT experiment_id, ear, tonotopicLocation, eid
		FROM Animal JOIN Experiment on subjectID = animal_id
		WHERE aid = {0};  
		'''.format(fs['aid'].value)
		
		expResults = query_gawa(query)
		
		### print page
		print_header()
		print '<div id = "animal-info" class = "info-sheet">'
		print '<h1>Subject ID: ' + str(animalResults[0][0]) + '</h1>'
		print '<ul id = "animal-info-list">'
		print '<li>species: ' + str(animalResults[0][1])  + '</li>' 
		print '<li>age: ' + str(animalResults[0][2])  + '</li>' 
		print '<li>weight: ' + str(animalResults[0][3])  + '</li>'
		print '<li>size: ' + str(animalResults[0][4])  + '</li>'
		print '<ul>' 
		print '</div>'
		
		print '<div id = "animal-experiments-info">'
		print '<table>'
		print '<tr><th>Experiment ID</th><th>ear</th><th>Tonotopic Location</th><tr>'
		for result in expResults:

			getString = '?toExperimentPage=true&eid=' + str(result[3])  #build GET string for URL	
			print '<tr>'
			for i in range(3):
				print '<td><a href = "browse.py' + getString + '">' + str(result[i]) + '</a></td>'
			print '</tr>'
		print '</table>'	
		print_footer()
		sys.exit()

	if fs.has_key('toExperimentPage'):
	
		# get experiment info	
		query = '''
			SELECT experiment_id, ear, tonotopicLocation, animal_id
			FROM Experiment
			WHERE eid = {0}	
		'''.format(fs['eid'].value)
		result = query_gawa(query)
		
		# print page
		print_header()
		print '<div id = "experiment-info" class = "info-sheet">'
		print '<h1>Experiment ID: ' + str(result[0][0]) + '</h1>'
		print '<ul id = "experiment-info-list">'
		print '<li>ear: ' + str(result[0][1])  + '</li>' 
		print '<li>Tonotopic Location: ' + str(result[0][2]) + '</li>' 
		print '<li>Animal ID: ' + str(result[0][3]) + '</li>'
		print '<ul>' 
		print_footer()
		sys.exit();
		

	if fs.has_key('toImagePage'):
	
		print_header()
                query = '''
                        SELECT experiment_eid, focalPlaneLevel, daqFreq
                        FROM Image
                        WHERE iid = {0};        
                         '''.format(fs['iid'].value) 
		
		results = query_gawa(query)	
		# get image set  
		query = '''
			SELECT imageFilename, timestamp, experiment_eid, prepInformation, focalPlaneRemarks, daqFreq 
			FROM Image
			WHERE experiment_eid = '{0}' AND focalPlaneLevel = {1} AND daqFreq = {2};
			'''.format(results[0][0], str(results[0][1]), str(results[0][2]))
		results = query_gawa(query)
		
		# build filepath array
		fileArray = []
		for result in results:
			fileArray.append(result[0])
		
		# USE FILEARRY TO MAKE GIF!!!!!!!!!!!!
		
		# chop end of file path for display
		filePath = str(results[0][0]);
		ind = filePath.rfind('\\')
		filePath = filePath[:ind]	
		
		#print page	
		print_header()		
		print '<div id = "image-group-info" class = "info-sheet">'
                print '<h1>Image Group File Path: ' + filePath + '</h1>'
                print '<ul id = "experiment-info-list">'
                print '<li>timestamp: ' + str(results[0][1])  + '</li>'
                print '<li>experiment id: ' + str(results[0][2]) + '</li>'
                print '<li>prep information: ' + str(results[0][3]) + '</li>' 
                print '<li>focalPlaneRemarks: ' + str(results[0][4]) + '</li>'
                print '<li>daqFrequency: ' + str(results[0][5]) + '</li>'
		print '<ul>'
                print '</div>'
		print_footer()
		sys.exit() 
	
	
	if fs.has_key('browse_by'): # then the user has just set a browse result type. print the relevent filter options
		
		resultType = fs['browse_by'].value
		if resultType == 'none': 
			sys.exit()
		if resultType == 'Image': # must group by on image queries to get image sets
			query = '''
				SELECT *, COUNT(*)
				FROM Image 
				GROUP BY experiment_eid, focalPlaneLevel, daqFreq; 
				'''

		else: #resultType = Animal, Experiment, or ROI 
			query = '''
			SELECT * 
			FROM %s; 
			''' % fs['browse_by'].value # Animal, Experiment, or Image
		
		results = query_gawa(query)

		query = '''
		SHOW COLUMNS FROM %s;
		''' % fs['browse_by'].value # Animal, Experiment, or Image
	
			
		columnNames = query_gawa(query)
		print_display_options(columnNames,resultType);	
		print_form(columnNames, results, resultType);
		print_table(columnNames, results, resultType);
		
	 	
	else: # user just filtered some results
		resultType = fs['browse'].value
		displayFields = []
                for key in fs:
                        if 'show_field' in key:
                                displayFields.append(key)

		query = '''
		SHOW COLUMNS FROM {0};
		'''.format(resultType) # Animal, Experiment, or Image
	
		cols = query_gawa(query)
		selectFields = ''
		for col in cols:
			selectFields += ',' + str(col[0])
		selectFields = selectFields[1:]
			
		if len(fs) == 1 + len(displayFields): # then the only field is the hidden field, and all parameters have been set to 'any'		
			if resultType == 'Image': 
				query = '''
				SELECT *, COUNT(*) 
				FROM Image
				GROUP BY experiment_eid, focalPlaneLevel, daqFreq; 
				'''
			else: #resultType = Animal, Experiment, or ROI  	

				query = '''
				SELECT * 
				FROM {0}; 
				'''.format(resultType)
		
		else:
			queryAttributes = ''
			for key in fs: 
				if key != 'browse' and 'show_field' not in key:
					queryAttributes += 'and ' + key + ' = "' + fs[key].value + '"'
			queryAttributes = queryAttributes[3:] #strip off first 'and'	
			if resultType == 'Image':
				
				query = '''
				SELECT *, COUNT(*)
				FROM Image
				WHERE {0}
				GROUP BY experiment_eid, focalPlaneLevel,  daqFreq;
				'''.format(queryAttributes)

			else: #resultType = Animal, Experiment, or ROI  	
				query = '''
				SELECT * 
				FROM {0}
				WHERE {1} ; 
				'''.format(resultType, queryAttributes) 
			
		results = query_gawa(query)

		
		if results: #query returned > 0 results
			
			resultType = fs['browse'].value	
			output = ''	
			for result in results:
				getString = '?to' + resultType + 'Page=true&'  #build URL string with result type and ID
				if resultType == 'Animal':
					getString += 'aid='
				elif resultType == 'Experiment':
					getString += 'eid='
				else: # resultType == 'Image'
					getString += 'iid=' 
				getString += str(result[0])
				output += '<tr class = "ajax-destroyable">'
				count = 0
				print '<p>'+ str(cols) + '</p>'
				print '<p>' + str(result) + '</p>'	
	
				for i in range(len(result)):# MAYBE - 1???ASDFSADFASFASDF	
					output += '<td class = ' + str(cols[i][0]) + '><a href = "' + getString + '">' + str(result[i]) + '</td>'
				output += '</tr>'
			print output
		else: #query returned nothing
			print '<p class = "ajax-destroyable">I\'m sorry, there are no items with those attributes.</p>'

else:
# then it is the user's first time on the page. 
# run initial query and display all results
# also populate the select menues with relevant choices.

	print_header()	
	print_browse_by_form()
	print_footer()



