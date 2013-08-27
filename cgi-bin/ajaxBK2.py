#!/usr/local/Python-2.7.3/bin/python

import cgi, random, os.path, cgitb, json, sys, MySQLdb
cgitb.enable() 
print "Content-type: text/html\n"

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

cursor, connection = connect_db('wrchapin', 'pad999')



# takes a results object and returns all values from a single column (used to get select options)
def get_column(results, index):
	col = []
	for result in results:
		col.append(result[index])
	return col
		
def print_form(cols, results, browse_by):
	#Print Browse Options Form	
	print '<form id = "form_options" class = "ajax-destroyable-options">'
	print '<input type = "hidden" name = "browse" value = "' + browse_by + '">'
	#loop through cols to get options
	for i in range(len(cols)):
		colHead = str(cols[i][0])
		colOptions = set(get_column(results, i)) #remove duplicates with set()
		if colHead == 'rid': #special case, making rid field into boolean has ROI field
			print '<label for = "' + colHead +'">has ROI:</label>'
			print '<select name = "' + colHead  + '" id = "' + colHead + '" class = "drawTableOnChange">'
		else:
			print '<label for = "' + colHead + '">' + colHead + ':</label>'
			print '<select name = "' + colHead  + '" id = "' + colHead + '" class = "drawTableOnChange">'
		print '<option value = "">any</option>'
		if colHead == 'rid':
			print '<option value = "yes">yes</option>'
			print '<option value = "no">no</option>'
		else:
			while (len(colOptions) != 0):
				option = str(colOptions.pop())
				print '<option value = "' + option + '">' + option + '</option>'
		print '</select>'	
	print '</form>'

def print_table(cols, results, browse_by, print_thead):
	#print titles
	

	if print_thead: #print the table header

		if (browse_by == 'Image'):
			print '<h2 class = "ajax-destroyable-options">' + browse_by + ' Sets</h2>'
		else:
			print '<h2 class = "ajax-destroyable-options">' + browse_by + 's</h2>'
		print '''
		<div id = "results-wrapper" class = "ajax-destroyable-options">
	        	<table id = "results">
				<thead><tr>'''
		for col in cols:
			if str(col[0]) == 'rid': # special case ROI
				print '<th class = "' + str(col[0]) + '">has ROI</th>'
			else:		
				print '<th class = "' + str(col[0]) + '">' + str(col[0]) + '</th>'
		
		print '</tr></thead><tbody>'
	
	
	

	# table below this point will be redrawn with ajax when user modifies parameters
	
	

	
	for j in range(len(results)):
	
		getString = 'to' + browse_by + 'Page=true&'  #built GET key/val pairs to place into the anchor tag
		getString += str(cols[0][0]) + '=' + str(results[j][0])	
		
		print '<tr class = "ajax-destroyable" onclick="TableRowLink(\'gawa.py?page=browse&' + getString + '\');">'
		for i in range(len(cols)-1):
			print '<td class = "' + str(cols[i][0]) + '">' + str(results[j][i]) + '</td>'
		#last column is has ROI
		print '<td class = "' + str(cols[-1][0]) + '">'
		if str(results[j][-1]) == 'None':
			print 'No' 
		else:
			print 'Yes'
		print '</tr>'

	if print_thead:
		print '</tbody></table>'
		print '</div>'

# prints the checkboxes that control the visible result fields
def print_display_options(cols, resultType):
	print '<div id = "display_options" class = "ajax-destroyable-options">'
	print '<div id = "navOpen">Display Options</div>'
	print '<div id = checkboxes>'
	print '<form id = "check_box_data">'
	for col in cols:
		print '<div class = checkbox-wrapper>'
		print '<input type = "checkbox" class = "checkbox" checked = "true" id = "' + col[0] + '" name = "show_field_' + col[0] + '" value = "on">'
		print '<label for = "' + col[0] + '">'
		if col[0] == 'rid':
			print 'has ROI'
		else:	
			print col[0] 
		print '</label>'
		print '</div>'
	print '</form>'
	print '</div>' # close checkboxes
	print '</div>' # close display_options

def query_gawa(query):
	cursor.execute(query)
	results = cursor.fetchall()
	return results
	

fs = cgi.FieldStorage()

if fs: # then the user has just changed a browsing parameter.
	
	if fs.has_key('browse_by'): # then the user has just set a browse result type. print the relevent filter options
		resultType = fs['browse_by'].value
		if resultType == 'none': 
			sys.exit()
		if resultType == 'Image': 
			resultQuery = '''
				SELECT *
				FROM Image NATURAL LEFT JOIN Image_has_ROI 
				GROUP BY experiment_eid, focalPlaneLevel, daqFreq
				LIMIT 1000; 
				'''	
		elif resultType == 'Experiment':  
			resultQuery = '''
				SELECT eid,ear,experiment_id,qualityIndex,qualityRemarks,tonotopicLocation,animal_id,rid 
				FROM (Experiment JOIN Image on experiment_id = experiment_eid) NATURAL LEFT JOIN Image_has_ROI
				GROUP BY eid; 
			'''

		elif resultType == 'Animal':
			resultQuery = '''
                                SELECT aid,weight,age,sex,drug,dose_mg_kg,postMortemActivity,Animal.remarks,subjectID species,rid
                                FROM ((Animal JOIN Experiment on subjectID = animal_id)
					 JOIN Image on experiment_id = experiment_eid) 
						NATURAL LEFT JOIN Image_has_ROI
                                GROUP BY aid; 
                        '''     
	
				
		results = query_gawa(resultQuery)	
		columnNames = cursor.description

		print_display_options(columnNames,resultType);	
		print_form(columnNames, results, resultType);
		print 'delimiter' #used in ajax.js, result splits on 'delimiter'
		print_table(columnNames, results, resultType, True);
	
		sys.exit();
	
	elif fs.has_key('browse'): # user just filtered some results
		resultType = fs['browse'].value
	
		# show_field given by display options checkboxs
		displayFields = []
                for key in fs:
                        if 'show_field' in key:
                                displayFields.append(key)
		
		if len(fs) == 1 + len(displayFields): # then the only field is the hidden field, and all parameters have been set to 'any'		
			if resultType == 'Image': 
				query = '''
				SELECT *
				FROM Image NATURAL LEFT JOIN Image_has_ROI 
				GROUP BY experiment_eid, focalPlaneLevel, daqFreq
				LIMIT 1000; 
				'''
			elif resultType == 'Experiment': #resultType = Animal, Experiment, or ROI  	
				query = '''
                                SELECT eid,ear,experiment_id,qualityIndex,qualityRemarks,tonotopicLocation,animal_id,rid 
                                FROM (Experiment JOIN Image on experiment_id = experiment_eid) NATURAL LEFT JOIN Image_has_ROI
				GROUP BY eid;
				''' 	
		else:
			queryAttributes = ''
			for key in fs: 
				if key != 'browse' and 'show_field' not in key:
					if 'rid' in key:
						if fs[key].value == 'no':
							queryAttributes += ' and ' + key + ' is null'
						if fs[key].value == 'yes':
							queryAttributes += ' and ' + key + ' != "None"'
					else: 
						queryAttributes += ' and ' + key + ' = "' + fs[key].value + '"'
			queryAttributes = queryAttributes[4:] #strip off first 'and '	
			if resultType == 'Image':
				
				query = '''
				SELECT *
                                FROM Image NATURAL LEFT JOIN Image_has_ROI 
                                WHERE {0}
                                GROUP BY experiment_eid, focalPlaneLevel, daqFreq
				LIMIT 1000;
				'''.format(queryAttributes)
			elif resultType == 'Experiment': #resultType = Animal, Experiment, or ROI  	
				query = '''
				SELECT eid,ear,experiment_id,qualityIndex,qualityRemarks,tonotopicLocation,animal_id,rid 
                                FROM (Experiment JOIN Image on experiment_id = experiment_eid) NATURAL LEFT JOIN Image_has_ROI
				WHERE {0} 
                                GROUP BY eid; 
				'''.format(queryAttributes)
		results = query_gawa(query)
		cols = cursor.description
		
		if results: #query returned > 0 results
			
			print_thead = False
			print_table(cols, results, resultType, print_thead)
		
		else: #query returned nothing
			print '<p class = "ajax-destroyable">I\'m sorry, there are no items with those attributes.</p>'

		
	if fs.has_key('drawImageInfo'):
		
		query = '''
		SELECT iid, timestamp, experiment_eid, prepInformation, focalPlaneRemarks, daqFreq, imageFilename 
                FROM Image
                WHERE experiment_eid = '{0}' AND focalPlaneLevel = {1} AND daqFreq = {2}; 
		'''.format(fs['eid'].value, fs['level'].value, fs['freq'].value, ) 

		results = query_gawa(query)

		print '<div id = "imagePage" class = "resultPage">'
                print '<div id = "image-group-info" class = "info-sheet">'
		print '<h2 id = "image-title"><a href = "gawa.py?page=browse&toImagePage=true&iid=' + str(results[0][0]) + '">Image Group Containing ' + str(results[0][0]) + '</a></h2>'
                print '<ul id = "experiment-info-list">'
		print '<li>timestamp: ' + str(results[0][1])  + '</li>'
                print '<li>experiment id: ' + str(results[0][2]) + '</li>'
                print '<li>prep information: ' + str(results[0][3]) + '</li>'
                print '<li>focalPlaneRemarks: ' + str(results[0][4]) + '</li>'
                print '<li>daqFrequency: ' + str(results[0][5]) + '</li>'
                print '<ul>'
                print '</div>'
	
	sys.exit()

 	
else:
# then it is the user's first time on the page. 
# run initial query and display all results
# also populate the select menues with relevant choices.

	print_browse_by_form()



