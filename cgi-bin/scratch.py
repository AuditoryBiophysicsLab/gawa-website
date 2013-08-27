#!/usr/local/Python-2.7.3/bin/python
import sys, MySQLdb, cgi, cgitb, re, random, string, datetime, os.path, json
cgitb.enable()

def print_head():
	print "Content-type: text/html\n"
	print "<html><head>"
	print "<link rel=\"stylesheet\" type=\"text/css\" href=\"/students_13/gawa/style_new.css\" />"
	print "<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>"
	print "<title>CHART TEST CODE</title>"
	print "</head><body>"

def print_tail():
	print "</body>"
	print "</html>"

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
	
def print_HTML_about_DB_Stats(dbstatid):
	if dbstatid == 1: # Number of Animals
		query = "SELECT COUNT(*) AS 'Number of Animals' FROM Animal;"
	if dbstatid == 2: # Number of Experiments
		query = "SELECT COUNT(*) AS 'Number of Experiments' FROM Experiment;"
	if dbstatid == 3: # Number of Images
		query = "SELECT COUNT(*) AS 'Number of Images' FROM Image;"
	
	#get and return results of query
	cursor.execute(query)
	results = cursor.fetchall()
	description = cursor.description

	# check to see if results exist
	if not results:
		print "<h3 class=\"error\">Sorry, your query did not return any results.</h3>"
	else:
		print "<h2 class='DBStats'> %s : %s </h2>" %(description[0][0],results[0][0])
	    
def print_HTML_about_charts(chartid):
	# get the data for the charts based on the chart id
	if chartid == 1: # Exp by Tono Location
		query = "SELECT tonotopicLocation AS 'Tonotopic Location', COUNT(*) AS COUNT FROM Experiment GROUP BY tonotopicLocation ORDER BY tonotopicLocation ASC;"
		chartoptions = "{title: 'Experiments by Tonotopic Location'};"
		divname = "chart_div_tono"
	if chartid == 2: # Histo of Animal Ages
		query = "SELECT age, COUNT(*) AS COUNT from Animal GROUP BY age ORDER BY age ASC;"
		chartoptions = "{title: 'Animals by Ages in Months'};"
		divname = "chart_div_animal_age"		
	if chartid == 3: # Animal Species
		query = "SELECT species AS 'Animal Species', COUNT(*) AS COUNT from Animal GROUP BY species ORDER BY species ASC;"
		chartoptions = "{title: 'Animals by Species'};"
		divname = "chart_div_animal_species"
	if chartid == 4: # Experiments with ROI
		query = "SELECT 'NO' AS 'ROI Exists', COUNT(*) AS 'Number of Experiments' FROM Experiment e LEFT JOIN (Image i NATURAL JOIN Image_has_ROI r) ON e.experiment_id = i.experiment_eid WHERE rid IS NULL UNION SELECT 'YES' AS 'ROI Exists', COUNT(*) AS 'Number of Experiments' FROM (SELECT eid FROM Experiment e LEFT JOIN (Image i NATURAL JOIN Image_has_ROI r) ON e.experiment_id = i.experiment_eid WHERE rid IS NOT NULL GROUP BY eid) AS X;"
		chartoptions = "{title: 'Experiments With Associated ROI Data', slices: [{color: 'red'}, {color: 'green'}]};"
		divname = "chart_div_exp_roi"
	if chartid == 5: # Images with ROI
		query = "SELECT 'No ROI' AS 'ROI Exists', COUNT(*) AS 'Number of Images' FROM Image NATURAL LEFT JOIN Image_has_ROI WHERE rid IS NULL UNION SELECT 'Has ROI' AS 'ROI Exists', COUNT(*) AS 'Number of Images' FROM (SELECT iid FROM Image NATURAL LEFT JOIN Image_has_ROI WHERE rid IS NOT NULL GROUP BY iid) AS X;"
		chartoptions = "{title: 'Images With Associated ROI Data', slices: [{color: 'red'}, {color: 'green'}]};"
		divname = "chart_div_img_roi"

	# define chart types
	piechartypes_byquery = [1,3,4,5]
	columncharts_byquery = [2]
		
	#get and return results of query
	cursor.execute(query)
	results = cursor.fetchall()

	#print an overriding container for CSS
	print "<div id='google_generated_chart'>"

	# check to see if results exist
	if not results:
			print "<h3 class=\"error\">Sorry, your query did not return any results.</h3>"
	else:
		print """<script type=\"text/javascript\">
			google.load(\"visualization\", \"1\", {packages:[\"corechart\"]});
			google.setOnLoadCallback(drawChart);
			function drawChart() {
			var data = google.visualization.arrayToDataTable(["""

		# print the results table	
		description = cursor.description
		descriptionitems = []
		for item in description:
			descriptionitems.append(item[0])
		print "['"+descriptionitems[0]+"', '"+descriptionitems[1]+"'],"		
		resultsitems = ""
		for item in results:
			Location = str(item[0])
			if Location == "":
				Location = "UNDEFINED"
			resultsitems += "['"+Location+"', "+str(item[1])+"],"
		resultsitems = resultsitems[:-1]
		print resultsitems
		print "]);"
		print "var options = "+chartoptions
		
		if chartid in piechartypes_byquery:
			print "var chart = new google.visualization.PieChart(document.getElementById('"+divname+"'));"
		elif chartid in columncharts_byquery:
			print "var chart = new google.visualization.ColumnChart(document.getElementById('"+divname+"'));"
	
		print """chart.draw(data, options);
			}
			</script>"""
		print "<div id='"+divname+"' class=\"google-chart\"></div>"	

	#print an overriding container for CSS, closing statement
	print "</div><!--END GOOGLE GENERATED CHART DIV-->"

### RUNNING PROGRAM CODE ###
#connect to DB and get cursor
cursor, connection = connect_db("jiwani","24horse!!")

print_head()

print "<div id='about_dbstats_container'>"

print "<div id='about_dbstats_header'>"
print "<h1>The GAWA Database</h1>"
print "<p>This page contains stats in the form of text and graphs.  All information was generated and was current at the time the page was loaded.</p>"
print "</div><!--END ABOUT DBSTATS HEADER CONTAINER-->"

print "<div id='dbstats_container'>"
print "<h2> Current Stats on the Number of the Database Entries</h2><ul>"
print_HTML_about_DB_Stats(1)  # Number of Animals in DB
print_HTML_about_DB_Stats(2)  # Number of Experiments in DB
print_HTML_about_DB_Stats(3)  # Number of Images in DB
print "</ul></div><!--END DBSTATS CONTAINER-->"

print "<div id='dbcharts_container'>"	
print "<h2> Graphical Representation of GAWA Data</h2>"
print "<div id='dbcharts_container_inner'>"	
print_HTML_about_charts(1)  # Pie Experiments by Tono Location
print_HTML_about_charts(2)  # Bar Animals by Days Age
print_HTML_about_charts(3)  # Pie Animals by Species
print_HTML_about_charts(4)  # Pie ROIs by Experiment
print_HTML_about_charts(5)  # Pie ROIs by Images
print "</div></div><!--END DBCHARTS CONTAINERS-->"

print "</div><!--END ABOUT DBSTATS CONTAINER-->"


print_tail()