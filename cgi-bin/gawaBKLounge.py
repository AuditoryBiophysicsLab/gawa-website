#!/usr/local/Python-2.7.3/bin/python
import sys, MySQLdb, cgi, cgitb, re, random, string, datetime, os, os.path, json, datetime
cgitb.enable()

####  THIS IS OUR FINAL PROJECT CODE ####
#### LAST MODIFIED ON  ####



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


### THESE DEFINITIONS ARE FROM GawaImage.py FROM AMAUCHE E. 5/2/13 2:30 PM ###

def htmlImageFolder():
        return '/www/html/students_13/gawa/'

def image_timeout():
	return 24*60*60*100000 #24 hours in deciseconds

def zip_timeout():
	return 24*60*60*100000 #24 hours in deciseconds

def createAnimatedGIF(strArr):
	if (not isinstance(strArr,list)):
		print "Input is not an array"
		return None
	if len(strArr)<1:
		print "Array cannot be empty"
		return []

	from PIL import Image
	from images2gif import writeGif

	resultArr = convertToGIF(strArr,700,fullPath=False)

	images = [Image.open(fn) for fn in resultArr]
	tempfolder = os.path.split(resultArr[0])[0]
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	dstPath = os.path.join(tempfolder,"my_gif"+epochtime+".GIF")
	output = writeGif(dstPath,images, duration=0.2)

	if(os.path.exists(dstPath)):
		return [getURLPath(dstPath)]
	else:
		print "I failed to create animated GIF "+filename
		return None

def convertToGIF(strArr,size=-1,fullPath=True):
	if (not isinstance(strArr,list)):
		print "Input is not an array"
		return None
	if len(strArr)<1:
		print "Array cannot be empty"
		return []

	import shutil
	from subprocess import call
	
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	tempfolder = os.path.join(htmlImageFolder(),"anigif",epochtime) 

	if not os.path.exists(tempfolder):os.makedirs(tempfolder)
	resultArr = []
	
	#This section removes all th directories created that are older than 6 minutes.
	for top, dirs, files in os.walk(os.path.dirname(tempfolder)):
	    for subd in dirs:
		if subd.isdigit(): 
			tstamp = int(subd)
			if int(datetime.datetime.now().strftime('%s%f'))-tstamp>image_timeout():
                                try :
                                        shutil.rmtree(os.path.join(top,subd))
                                except :
                                        pass


	for fiPath in strArr:
		if fiPath.endswith('.tif'):
			
			justName = os.path.split(fiPath)[-1].split('.')[0]
			dstPath = os.path.join(tempfolder,justName + ".gif")
			if os.path.exists(dstPath):os.remove(dstPath)			
			if(size is None or not isinstance(size,int) or size < 0):
				output = call(["/usr/bin/convert",fiPath, dstPath])
			else:
				output = call(["/usr/bin/convert","-resize",str(size)+"x"+str(size),fiPath, dstPath])

			if(os.path.exists(dstPath)):
				if(fullPath): dstPath = getURLPath(dstPath)
				resultArr.append(dstPath)

	return resultArr

def convertToThumb(strArr,fullPath=True):
	return convertToGIF(strArr,size=200,fullPath=fullPath)

def copyTifFile(strArr):
	from shutil import copyfile
	output = []
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	tempfolder = os.path.join(htmlImageFolder(),"anigif",epochtime)
        if not os.path.exists(tempfolder):os.makedirs(tempfolder)

	for fi in strArr:
		dest = os.path.join(tempfolder,os.path.split(fi)[-1])
		copyfile(fi, dest)
		if not os.path.exists(dest):
			print "I didn't copy the file correctly"
		output.append(getURLPath(dest))
	return output

def zipImages(sourceFolder):
	import zipfile
	epochtime = str(datetime.datetime.now().strftime('%s%f'))
	dfolder = os.path.join(htmlImageFolder(),'zips')
	if not os.path.exists(dfolder):os.makedirs(dfolder)
	dfile = os.path.join(dfolder,epochtime+".zip")
	zf = zipfile.ZipFile(dfile, "w")
	containFolder = os.path.abspath(sourceFolder)
	for dirname, subdirs, files in os.walk(containFolder):
	        for filename in files:
			filepath = os.path.abspath(os.path.join(dirname, filename))
			zf.write(filepath, filename)
	zf.close()

	#This section removes all the files created that are older than 2 minutes.
        for top, dirs, files in os.walk(dfolder):
            for file in files:
		fname = file.split('.')[0]
                if fname.isdigit():
                        tstamp = int(fname)
                        if int(datetime.datetime.now().strftime('%s%f'))-tstamp>zip_timeout():
                                try :
					os.remove(os.path.join(top,file))
				except :
					pass
	return getURLPath(dfile)

def print_to_file(strArr):
        epochtime = str(datetime.datetime.now().strftime('%s%f'))
        dfolder = os.path.join( htmlImageFolder(),'anigif')
        if not os.path.exists(dfolder):os.makedirs(dfolder)

        txtfile = os.path.join(dfolder,epochtime+".txt")
        text_file = open(txtfile, "w")
        for filepath in strArr:
                text_file.write(filepath+'\n')
        text_file.close()


        #Remove old text fiels
        for dirname, subdirs, files in os.walk(dfolder):
                for filename in files:
                        filename = filename.split('.')[0]
                        if filename.isdigit():
                                tstamp = int(filename)
                                if int(datetime.datetime.now().strftime('%s%f'))-tstamp>image_timeout():
                                        try :
                                                os.remove(os.path.join(dirname,filename))
                                        except :
                                                pass

        if(os.path.exists(txtfile)):
                return getURLPath(txtfile)
        return None



def getURLPath(path):
	str1 = path.split('html/')[-1]
	httpAdr = "http://bioed.bu.edu/"
	dstPath = httpAdr+str1
	return dstPath

### ROI CODE ###

def printROIHeader():
	print """
	<script>
	$(document).ready(function(){
		function scrollList(element){
			var rowpos = $("#RIOTable #"+element).position();
			var scrollTop = $("#RIOTable").scrollTop();
			var scrollBottom  = scrollTop + $("#RIOTable").height();
			var itembottom = rowpos.top + $("#RIOTable #"+element).height();
			if(rowpos.top<scrollTop || itembottom >=scrollBottom){
				$("#RIOTable").scrollTop(rowpos.top);
			}
		}
		function scrollImage(element){
			var el = $("#ROIimage #"+element);
			var scrl = $("#ROIimage");

			var rowpos = el.position();
			var scrollTop = scrl.scrollTop();
			var scrollBottom  = scrollTop + scrl.height();
			var itembottom = rowpos.top + el.height();

			if(rowpos.top<scrollTop || itembottom >=scrollBottom){
				scrl.scrollTop(rowpos.top);
			}

			var scrollLeft = scrl.scrollLeft();
			var scrollRight  = scrollLeft + scrl.width();
			var itemright = rowpos.left + el.width();

			if(rowpos.left<scrollLeft || itemright >=scrollRight){
				scrl.scrollLeft(scrollLeft + rowpos.left);
			}

		}
	
                function highlightTableElement(element) {
                        $("#RIOTable #"+element).css('background', '#C1A3A5');
			$("#ROIimage a#"+element).addClass('mouseover');
                }

                function clearTableElement(element) {
                        $("#RIOTable #"+element).css('background', '#FFFFFF');
			$("#ROIimage a#"+element).removeClass('mouseover')
                }

		function printLink(element){
			var hlink = $("#ROIimage a#"+element+" span").attr('id');
			$('#RIOTable .selected').removeClass('selected');
			$('#RIOTable #'+element+" td").addClass('selected');
			$('#ROIimage .selected').removeClass('selected');
			$('#ROIimage a#'+element).addClass('selected');
			var infoSection = $("#ROIinformation span");
			infoSection.html("");
			infoSection.append(hlink);
		}

		$("#ROIimage a").bind("mouseover", function() {highlightTableElement($(this).attr('id'));});
		$("#ROIimage a").bind("mouseout", function() {clearTableElement($(this).attr('id'));});
		$("#RIOTable .listItem").bind("mouseover", function() {highlightTableElement($(this).attr('id'));});
		$("#RIOTable .listItem").bind("mouseout", function() {clearTableElement($(this).attr('id'));});
		$("#RIOTable .listItem").bind("click", function(){
			var elID = $(this).attr('id');
			printLink(elID);
			scrollImage(elID);
		});
		$("#ROIimage a").bind("click", function() {
			var elID = $(this).attr('id');
			printLink(elID);
			scrollList(elID);
		});
	});

	</script>
	"""

def printBody(imagePath,ROIDict,ROIProp):
	imageLink,listLink = getROIHtml(ROIDict)

	print """
	<div id="ROIPage_wrapper_outer">
	<div id="ROIPageTitle" >
	
	<h2>Specific ROI Title</h2>
	</div>"""
	printROITable(listLink)
	print"""
	<div id="ROIimage">
	<img src="%s" alt="Regions Of Interest Image">
	
	"""%(imagePath)
	
	print imageLink
	print "</div>"

	printROIinfoSection(ROIProp)
	print """</div>"""


def getROIHtml(ROIDict):
	imageLink =""
	tablerows =""

	for item in ROIDict:
		someID = item['ID']
		xpos = str(item['xpos'])
		ypos = str(item['ypos'])
		dx = str(item['dx'])
		dy = str(item['dy'])
		identifier = item['identifier']

		imageLink += """
		<a id="%s" title="Region %s" style="left:%spx;top:%spx;height:%spx;width:%spx;">
		<span id="ROI #%s (%s,%s)"/>
		</a>"""%(someID,identifier,xpos,ypos,dx,dy,identifier,xpos,ypos)

		tablerows+="""
		<tr class="listItem" id="%s">
		<td><a><span>Region %s</span></a></td>
		</tr> """ %(someID,identifier)

	return imageLink,tablerows

def printROITable(tablerows):
	print """
	<div id="RIOTable">
	<table cellspacing="0" cellpadding="1" border="1">
	"""
	print tablerows
	
	print """
	</table>
	</div>"""

def printROIinfoSection(ROIProp):
	print """
	<div id="ROIinformation">
	<h2><span id="name">ROI Information:</span></h2>"""
	
        print '<table border="0">'
        for key in ROIProp:
                print '<tr><td><b>%s: </b></td><td>%s</td></tr>'%(key,ROIProp[key])
        print'</table>'

	print "	</div>"



### SESSION CODE FROM AMAUCHE GOES HERE ###
import gawa_session


### BROWSE FUNCTION CODE FROM WILL THAT NEED TO BE INCLUDED HERE ### 
def query_gawa(query):
        cursor.execute(query)
        results = cursor.fetchall()
        return results

def get_column(results, index):
        col = []
        for result in results:
                col.append(result[index])
        return col

def print_browse_by_form():
        print '<form id = "form_browse_by">'
        print '<h1>BROWSE BY: <a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help#browse\"><img src=\"/students_13/gawa/images/questionmark-dark-mini.png\"></a></h1>'
        print '<select name = "browse_by" id = "browse_by" class = "drawOptionsOnChange">'
        print '<option value = "none">Select Result Type</option>'
        print '<option value = "Animal">Animal</option>'
        print '<option value = "Experiment">Experiment</option>'
        print '<option value = "Image">Image</option>'
        print '<input type = "hidden" value = "browse" name = "page">'
        print '<input type = "hidden" value = "yes" name = "ajax">'
        print '</select>'
        print '</form>'

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

### ABOUT FUNCTION BUILDING CODE ###

# Print me some google chart goodness
def print_HTML_about_charts(chartid):
	# get the data for the charts based on the chart id
	if chartid == 1: # Exp by Tono Location
		query = "SELECT tonotopicLocation AS 'Tonotopic Location', COUNT(*) AS COUNT FROM Experiment GROUP BY tonotopicLocation ORDER BY tonotopicLocation ASC;"
		chartoptions = "{title: 'Experiments by Tonotopic Location'};"
		divname = "chart_div_tono"
	if chartid == 2: # Histo of Animal Ages
		query = "SELECT age, COUNT(*) AS COUNT from Animal GROUP BY age ORDER BY age ASC;"
		chartoptions = "{title: 'Animals by Ages in Days'};"
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


# print me some DB Stats goodness
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
		print "<li> %s : %s </li>" %(description[0][0],results[0][0])


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
	print "<script type=\"text/javascript\" src=\"http://code.jquery.com/jquery-1.9.1.min.js\"></script>"
	print "<script type=\"text/javascript\" src=\"/students_13/gawa/browse.js\"></script>"
	print "<script type=\"text/javascript\" src=\"/students_13/gawa/jquery.validate.js\"></script>"
	print "<script type=\"text/javascript\" src=\"https://www.google.com/jsapi\"></script>"
	printROIHeader() #load amauche's roi js code
	print """<script type=\"text/javascript\">
		function TableRowLink(theUrl)
		{
		document.location.href = theUrl;
		}
  </script>"""
	print "</head>"
	print "<body>"
	
def print_HTML_header_login_logo_pre():
	print "<div id=\"header\">"
	print "<div id=\"login\">"

def print_HTML_header_login_logo_post():
	print "</div>  <!--HEADER LOGIN END-->"
	print "<div id=\"logo\"><a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\"><img src=\"/students_13/gawa/images/gawa-logo2s.png\" width=\"208\" height=\"67\" alt=\"logo\" /></a></div>"
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
		query = "SELECT iid, focalPlaneLevel, focalPlaneRemarks, remarks, experiment_eid FROM Image NATURAL LEFT JOIN Image_has_ROI WHERE rid IS NULL;"
		query_desc = "List of images without ROIs"
	if qqueryid == 2:
		query = "SELECT * FROM Experiment;"
		query_desc = "All Experiments"
	if qqueryid == 3:
		query = "SELECT eid, experiment_eid, focalPlaneLevel, focalPlaneRemarks, remarks FROM Image JOIN Experiment ON experiment_id = experiment_eid GROUP BY experiment_eid, focalPlaneLevel, focalPlaneRemarks, remarks;"
		query_desc = "Image Remarks Grouped by Experiment and Focal Plane"
	if qqueryid == 4:
		query = "SELECT e.eid, e.experiment_id, e.tonotopicLocation, e.qualityIndex, e.qualityRemarks FROM Experiment e LEFT JOIN (Image i NATURAL JOIN Image_has_ROI r) ON e.experiment_id = i.experiment_eid WHERE rid IS NULL;"
		query_desc = "Experiments with no ROIs associated"
	if qqueryid == 5:
		query = "SELECT e.eid, e.experiment_id, e.ear, e.animal_id, e.qualityIndex, e.qualityRemarks FROM Experiment e WHERE e.tonotopicLocation IS NULL OR tonotopicLocation = \"\";"
		query_desc = "Experiments without Tonotopic Location Defined"
	if qqueryid == 6:
		query = "SELECT e.eid, i.experiment_eid, e.qualityIndex, e.qualityRemarks, i.focalPlaneLevel, i.focalPlaneRemarks, i.remarks FROM Image i JOIN Experiment e ON e.experiment_id = i.experiment_eid WHERE (focalPlaneRemarks REGEXP '%s') OR (remarks REGEXP '%s') GROUP BY experiment_eid, focalPlaneLevel, focalPlaneRemarks, remarks;" %(param1,param1)
		query_desc = "Experiments containing focal planes with physiological feature \"%s\"" %(param1)
	if qqueryid == 7:
		query = "SELECT eid, X.experiment_eid, qualityIndex, qualityRemarks, COUNT(*) AS COUNT FROM Experiment e JOIN (SELECT DISTINCT experiment_eid, focalPlaneLevel FROM Image) AS X ON e.experiment_id = X.experiment_eid GROUP BY eid HAVING COUNT >='%s';" %(param1)
		query_desc = "Experiments with %s or more focal planes" %(param1)
	if qqueryid == 8:
		query = "SELECT eid, experiment_id, qualityIndex, qualityRemarks FROM Experiment WHERE tonotopicLocation = \"%s\";" %(param1)
		query_desc = "Experiments at %s Tonotopic Location" %(param1)
	if qqueryid == 9:
		query = "SELECT iid, focalPlaneLevel, focalPlaneRemarks, remarks, experiment_eid FROM Image WHERE daqFreq = \"%s\" AND ((focalPlaneRemarks REGEXP '%s') OR (remarks REGEXP '%s')); " %(param1,param2,param2)
		query_desc = "Images taken at frequency %sHz containing focal planes with physiological feature \"%s\"" %(param1,param2)

	# Define which queries need links for animal pages, experiment pages or image pages, using qqueryid
	# use below to speed up which link type to print
	animal_queries_list = []
	experiment_queries_list = [2,3,4,5,6,7,8] 
	image_queries_list = [1,9]

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
			# prints links for image tables
			if qqueryid in image_queries_list:
				print "<tr onclick=\"TableRowLink('gawa.py?page=browse&toImagePage=true&iid=%s');\">" %(item[0])
			# prints links for experiment tables
			elif qqueryid in experiment_queries_list:
				print "<tr onclick=\"TableRowLink('gawa.py?page=browse&toExperimentPage=true&eid=%s');\">" %(item[0])
			# if you forget to define the results into the types above, then table with no links
			else:
				print "<tr>"
			for i in range(len(item)):
				print "<td>",item[i],"</td>"
			print "</tr>"
		print "</table>"

# this builds the selection lists for the semi-quick-queries
def semi_quick_query_list_builder(param=0):
	# determine which list to build
 	if param == 1:  # list of focal plane levels
 		query = "SELECT DISTINCT focalPlaneLevel FROM Image ORDER BY focalPlaneLevel ASC;"
 	if param == 2: #list of image frequencies
 		query = "SELECT DISTINCT daqFreq FROM Image ORDER BY daqFreq ASC;"
 	if param == 3: # list of tonotopic map locations
 		query = "SELECT DISTINCT tonotopicLocation FROM Experiment WHERE tonotopicLocation IS NOT NULL AND tonotopicLocation <> \"\" ORDER BY tonotopicLocation ASC;"
	
	#get and return results of query
	cursor.execute(query)
	results = cursor.fetchall()

	# check to see if results exist
	if not results:
			print "Sorry, your query did not return any results."
	else:
		# print the results table	
		for item in results:
			print "<option value=\"%s\">%s</option>" %(item[0],item[0])

def print_HTML_quickquery():
	print """<div id='searchbox'>
	<div class='quick-search'>
	<h1>QUICK SEARCH <a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help#quick_search\"><img src=\"/students_13/gawa/images/questionmark-dark-mini.png\"></a></h1>
	<form name="quicksearch" action="http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py" method="POST"> 
	<select name='quicksearchoption'>
	<option value='cat-1'>Noted Physiological Features</option>
	</selct>
	<input name="quicksearchkeyword" placeholder="keyword" type="text" />
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	</div> <!--END QUICK-SEARCH-->
	<div class='quick-query'>
	<h1>QUICK QUERIES <a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help#quick_query\"><img src=\"/students_13/gawa/images/questionmark-dark-mini.png\"></a></h1>
	<form name=\"quickquery\" action=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py\" method=\"POST\">
	<select name='quickqueryoption'>
	<option value='q2'>All Experiments</option>
	<option value='q5'>Experiments without a Tonotopic Location</option>
	<option value='q4'>Experiments without ROI</option>	
	<option value='q3'>Remarks by Experiment & Focal Plane</option>	
	<option value='q1'>Images without ROI</option>
	</select>
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	</div> <!--END QUICK-QUERIES-->
	<div class='semi-quick-query'>
	<h1>SEMI QUICK QUERIES <a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help#semi_quick_query\"><img src=\"/students_13/gawa/images/questionmark-dark-mini.png\"></a></h1>
	<form name="semiquickquery" action="http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py" method="POST">
    <label>Find all images whose Tonotopic Map has: </label></br>
	<select class='width170' name='tonotopic_map'>"""
	
	semi_quick_query_list_builder(param=3)  #builds tonotopic map selection list

	print """</select>
	<input name="semiquickquery" type="hidden" id="hiddenField" value="semiquickquery" />
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	<form name="semiquickquery" action="http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py" method="POST">
    <label>Find all images whose frequency is: </label></br>
	<select name='imagefrequency'>"""

	semi_quick_query_list_builder(param=2)  #builds frequency selection list

	print """</select>
    <label>And whose remarks contain: </label>
    <input name="remark" placeholder="keyword" type="text" />
    <input name="semiquickquery" type="hidden" id="hiddenField" value="semiquickquery" />
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	<form name="semiquickquery" action="http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py" method="POST">
    <label>Find all experiments with a minimum # of levels</label></br>
	<select class='width170' name='minlevelcount'>"""

	semi_quick_query_list_builder(param=1)  #builds level count selection list
	
	print """</select>
	<input name="semiquickquery" type="hidden" id="hiddenField" value="semiquickquery" />
	<input type='image' name='submit' src='/students_13/gawa/images/go.png'>
	</form>
	</div> <!--END SEMI-QUICK-QUERY-->
	</div> <!--END SEARCHBOX - NOT TO BE USED FOR CSS-->"""
	
	
### NULL QUERY ERROR PRINTER ###
def print_HTML_null_query_error():
	print """<div id='red-warning'><img src='http://bioed.bu.edu/students_13/gawa/images/warning2.png' /><br>
		<p class='error'>Null queries are not allowed.  Please try again.</p></div>"""		

### HTML ABOUT PROJECT PAGE, NOW PART OF HOME PAGE ###

def print_HTML_about_page():
	about_file = open('/www/html/students_13/gawa/about_html.txt', 'r')
	for line in about_file:
		print line
	about_file.close()

### HTML HELP PAGE ###

def print_HTML_help_sidebar():
	print """<div id='helplinkbox'>
	<h1>Help Pages</h1>
	<p> Select from the list below to learn more about how each works </p>
	<ul>
	<li><a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help\">Search & Queries</a></li>
	<li><a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help\">Browse Functions</a></li>
	<li><a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help3\">Update Functions</a></li>
	<li><a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help4\">HTML/CSS Design</a></li>
	<li><a href=\"http://bioed.bu.edu/cgi-bin/students_13/gawa/gawa.py?page=help5\">Python Code</a></li>
	</ul>
	</div> <!--END HELPLINKBOX-->"""

def print_HTML_help_page():
	help_file = open('/www/html/students_13/gawa/help_html.txt', 'r')
	for line in help_file:
		print line
	help_file.close()


### RUNNING PROGRAM CODE ###
#connect to DB and get cursor
cursor, connection = connect_db("jiwani","24horse!!")

# first get the form
form = cgi.FieldStorage()

#print beginning html
print_HTML_head()
print_HTML_header_login_logo_pre() 

# login form info
if (form.has_key("session_key")): 
	if (form.has_key("Logout")):
		gawa_session.delete_session(form["session_key"].value)
		gawa_session.generate_login_form() 
	else:
		u_id = gawa_session.fetch_username(form["session_key"].value)
		gawa_session.display_page("passed", u_id, form["session_key"].value)
elif (form.has_key("action") and form.has_key("username") and form.has_key("password")):
	result = gawa_session.test_passwd(form["username"].value, form["password"].value)
	gawa_session.display_page(result, form["username"].value) 
else:
	gawa_session.generate_login_form()
	
print_HTML_header_login_logo_post()

# print navigation & check to see if the user has been here, if not, set default to home
if "page" in form:
	current_page = form["page"].value
else:
	current_page = "home"
print_HTML_navigation(current_page)

#if current page is home, then...
if current_page == "home":
	print_HTML_content_pre()
	print_HTML_quickquery()
	print_HTML_content_mid()
	
	# check to see if quickqueryoption was used, if so, get its value and then run the query and return the results
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
	# if not print the about text
	elif "quicksearchoption" in form:
		qquery = form["quicksearchoption"].value
		try: 
			qsearchby = form["quicksearchkeyword"].value
			if qsearchby.strip() == "":
				print_HTML_null_query_error()
			elif qquery == "cat-1":
				quickquery_run(qqueryid=6,param1=qsearchby)
		except:
			print_HTML_null_query_error()
	elif "semiquickquery" in form:
		if "minlevelcount" in form:
			qsearchby = form["minlevelcount"].value
			quickquery_run(qqueryid=7,param1=qsearchby)
		if "tonotopic_map" in form:
			qsearchby = form["tonotopic_map"].value
			quickquery_run(qqueryid=8,param1=qsearchby)
		if "imagefrequency" in form:
			qsearchby = form["imagefrequency"].value	
			try: 
				qsearchkey = form["remark"].value
				if qsearchkey.strip() == "":
					print_HTML_null_query_error()
				else:
					quickquery_run(qqueryid=9,param1=qsearchby,param2=qsearchkey)
			except:
				print_HTML_null_query_error()
			
			
	else:
		print_HTML_about_page()
		
	print_HTML_content_post()

# check to see if the current page is about, if so, then print the about page
elif current_page == "about":
	print_HTML_content_single_pre()

	print "<div id='about_dbstats_container'>"
	
	print "<div id='about_dbstats_header'>"
	print "<h1>The GAWA Database</h1>"
	print "<p>Enjoy stats in the form of text and graphs which contain information that was generated upon loading this page.</p>"
	print "<p>The page uses the <a href='https://developers.google.com/chart/'>Google Chart Tools API.</a></p>"
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
	
	print_HTML_content_single_post()

# check to see if the current page is help, if so, then print the help page
elif current_page == "help":
	print_HTML_content_pre()
	print_HTML_help_sidebar()
	print_HTML_content_mid()
	print_HTML_help_page()
	print_HTML_content_post()


if current_page == "update":
	print_HTML_content_single_pre()
	print """<div id=\"red-warning\"><img src=\"http://bioed.bu.edu/students_13/gawa/images/warning2.png\" /><br>
		You have to be an administrator and logged in to use this page!</div>"""
	print_HTML_content_single_post()


### BROWSE EXECUTION CODE FROM WILL TO GO HERE ###
### BROWSE FUNCTIONS TO REMAIN WITHIN BROWSE.PY AS POSSIBLE ###
### CODE FOR EXPERIMENT, ANIMAL AND IMAGE PAGES SHOULD BE SEP FUNCTIONS ABOVE ####
### OTHERWISE SEE ABOVE ###

if current_page == "browse":
	if 'toAnimalPage' in form:
		print_HTML_content_single_pre()
                ### get animal info
                query = '''
                SELECT subjectID, species, age, weight, sex, drug, dose_mg_kg, postMortemActivity, remarks
                FROM Animal 
                Where aid = {0}
                '''.format(form['aid'].value)

                animalResults = query_gawa(query)

                ### get experiments associated with this animal
                query = '''
                SELECT experiment_id, ear, tonotopicLocation, eid
                FROM Animal JOIN Experiment on subjectID = animal_id
                WHERE aid = {0};  
                '''.format(form['aid'].value)

                expResults = query_gawa(query)

                print '<div id = "animalPage" class = "resultPage">'
                print '<div id = "animal-info" class = "info-sheet">'
                print '<h2>Subject ID: ' + str(animalResults[0][0]) + '</h2>'
                print '<ul class = "result-info-list">'
                print '<li>species: ' + str(animalResults[0][1])  + '</li>'
                print '<li>age: ' + str(animalResults[0][2])  + '</li>'
                print '<li>weight: ' + str(animalResults[0][3])  + '</li>'
                print '<li>sex: ' + str(animalResults[0][4])  + '</li>'
                print '<li>drug: ' + str(animalResults[0][5])  + '</li>'
                print '<li>dose_mg_kg: ' + str(animalResults[0][6])  + '</li>'
                print '<li>postMortemActivity: ' + str(animalResults[0][7])  + '</li>'
                print '<li>remarks: ' + str(animalResults[0][8])  + '</li>'
                print '</ul>'
                print '<table>'
                print '<thead><tr><th>Experiment ID</th><th>ear</th><th>Tonotopic Location</th></tr></thead>'
		print '<tbody>'
                for result in expResults:
                        getString = '?page=browse&toExperimentPage=true&eid=' + str(result[3]) 
			print '<tr onclick="TableRowLink(\'gawa.py' + getString + '\');">'
                        for i in range(3):
                                print '<td>' + str(result[i]) + '</td>'
                        print '</tr>'
		print '</tbody>'
                print '</table>'
                print '</div>'
		print '</div>'
		print_HTML_content_single_post()
		print_HTML_tail()
                sys.exit()

	elif form.has_key('toExperimentPage'):
		print_HTML_content_single_pre()
                # get experiment info   
                query = '''
                        SELECT experiment_id, ear, tonotopicLocation, qualityIndex, qualityRemarks, animal_id
                        FROM Experiment
                        WHERE eid = {0};
                '''.format(form['eid'].value)
                result = query_gawa(query)

                expID = str(result[0][0])


                #get aid for the amimal page link

                query = '''
                        SELECT aid
                        FROM Animal join Experiment on subjectID = animal_id
                        WHERE eid = '{0}'; 
                '''.format(form['eid'].value)
                aid = query_gawa(query)

                # print page

		print '<div id = "experimentPage" class = "resultPage">'
                print '<div id = "experiment-info" class = "info-sheet">'
                print '<h2>Experiment ID: ' + expID + '</h2>'
                print '<ul class = "result-info-list">'
                print '<li>ear: ' + str(result[0][1])  + '</li>'
                print '<li>Tonotopic Location: ' + str(result[0][2]) + '</li>'
                print '<li>Quality Index: ' + str(result[0][3]) + '</li>'
                print '<li>Quality Remarks: ' + str(result[0][4]) + '</li>'
                print '<li><a href = "gawa.py?page=browse&toAnimalPage=true&aid=' + str(aid[0][0]) + '">'
                print 'Animal ID: ' + str(result[0][5])
                print '</a></li>'
                print '</ul>'
                print '</div>'
		
                # get availible plane levels from DB for this experiment
                query = '''
                        SELECT focalPlaneLevel, experiment_eid
                        FROM Image
                        WHERE experiment_eid = '{0}'
                        GROUP BY focalPlaneLevel;
                        '''.format(expID)

                results = query_gawa(query)
		print '<div id = "level_freq_img_wrap">'
                print '<div id = "experiment_page_levels">'
                print '<table>'
		print '<thead><tr><th>Availible Focal Plane Levels</th></tr></thead>'
                print '<tbody>'
		for result in results:
                        print '<tr id = "' + str(result[0]) + '" class = "experiment_page_level ' + str(result[1]) + '"><td>' + str(result[0]) + '</td></tr>'
                print '</tbody>'
		print '</table>'
                print '</div>'

                #get availible freqs from DB for this experiment
                query = '''
                        SELECT daqFreq, experiment_eid
                        FROM Image
                        WHERE experiment_eid = '{0}'
                        GROUP BY daqFreq;
                        '''.format(expID)

                results = query_gawa(query)

                print '<div id = "experiment_page_frequencies">'
                print '<table><thead><tr>'
		print '<th>Availible Frequencies</th>'
		print '</tr></thead>'
                print '<tbody>'
                for result in results:
                        print '<tr id = "' + str(result[0]) + '" class = "experiment_page_freq ' + str(result[1]) + '"><td>' + str(result[0]) + '</td></tr>'
                print '</tbody>'
		print '</table>'
                print '</div>'
		# print div for image info
                print '<div id = "experiment_page_image_info"></div>'
		
		print '</div>'#close level_frequency_img_wrap div
		print '</div>'
		print_HTML_content_single_post()
		print_HTML_tail()
                sys.exit()
	
	elif form.has_key('toImagePage'):

		print_HTML_content_single_pre()
                query = '''
                        SELECT experiment_eid, focalPlaneLevel, daqFreq, subjectID, eid, aid
                        FROM (Image JOIN Experiment ON experiment_eid = experiment_id) JOIN Animal on animal_id = subjectID  
                        WHERE iid = {0};        
                         '''.format(form['iid'].value)
		
                results = query_gawa(query)

		subjectID = results[0][3]
                eid = results[0][4]
		aid = results[0][5]

		# get image set  
                query = '''
                        SELECT imageFilename, experiment_eid, timestamp, prepInformation, focalPlaneRemarks, daqFreq 
                        FROM Image
                        WHERE experiment_eid = '{0}' AND focalPlaneLevel = {1} AND daqFreq = {2};
                        '''.format(results[0][0], str(results[0][1]), str(results[0][2]))
                results = query_gawa(query)
		

		query = '''
			SELECT DISTINCT ROISerial
			FROM ROI NATURAL JOIN Image_has_ROI
			WHERE iid = {0} 
			'''.format(form['iid'].value)

		rids = query_gawa(query)
                
		# build filepath array
                fileArray = []
                for result in results:
                        fileArray.append(result[0])

		
                # chop end of file path for display
                filePath = str(results[0][0]);
                ind = filePath.rfind('/')
                filePath = filePath[:ind]

                #print page     
                print '<div id = "imagePage" class = "resultPage">'
                print '<h2>Image Group File Path: ' + filePath + '</h2>'
		print '<div id = "image-group-info" class = "info-sheet">'
                print '<ul id = "experiment-info-list">'
                print '<li><a href = "gawa.py?page=browse&toExperimentPage=true&eid=' + str(eid) + '">experiment id: ' + str(results[0][1]) + '</a></li>'
                print '<li><a href = "gawa.py?page=browse&toAnimalPage=true&aid=' + str(aid) + '">animal id: ' + str(subjectID) + '</a></li>'
                print '<li>timestamp: ' + str(results[0][2])  + '</li>'
                print '<li>prep information: ' + str(results[0][3]) + '</li>'
                print '<li>focalPlaneRemarks: ' + str(results[0][4]) + '</li>'
                print '<li>daqFrequency: ' + str(results[0][5]) + '</li>'
                if rids:
			print '<ul>'
                	for rid in rids:
				print '<li><a href = "gawa.py?page=browse&toROIPage=true&iid=' + form['iid'].value + '&eid=' + eid + '&rid=' + rid + '">has region of interest: yes</a></li>'
			print '</ul>'	
		print '<ul>'
                print '</div>'


                output = createAnimatedGIF(fileArray)
		print '<div id = gif-and-thumb-wrap>'
		print '<div id = "gifWrap">'
                for str1 in output:
                        print "<img src=\"%s\" alt=\"\">"%(str1)
                print '</div>'

		print "<div id='image_thumbnails'>"
 		gifFiles = convertToGIF(fileArray,84)
		tifFiles = copyTifFile(fileArray)
		for ite in range(len(fileArray)):
			print "<a class = 'thumbnail' href=\"%s\"><img src=\"%s\" alt=\"\"></a>"%(tifFiles[ite],gifFiles[ite])
		print '</div>'
		print '<div id = "butWrap">'
		print '<a href=\"%s\">download file paths</a>'%(print_to_file(fileArray))
 		print '<a href=\"%s\">download all images</a>'%(zipImages(filePath))
		print '</div>'

	
		print '</div>' #close gif-and-thumb-wrap
		print "</div> <!--IMAGE THUMBNAIL END-->"
		print '</div>' #close id = "imagePage"
		print "<div class='clearme'></div>"
		
		print_HTML_content_single_post() 
		print_HTML_tail()
		sys.exit()

	elif form.has_key('toROIPage'):
		iid = form['iid'].value	
		query = '''
			SELECT experiment_eid 
			FROM Image
			WHERE iid = {0}  
			'''.format(iid)

		eid = str(query_gawa(query)[0][0])
	
		query = '''
			SELECT ROISerial
			FROM ROI NATURAL JOIN Image_has_ROI
			WHERE iid = {0}
			'''.format(iid)	
		rid = str(query_gawa(query)[0][0])

		RoiProps = {'Experiment ID':eid,'ROI Serial':rid,'Image ID':iid}
		query1 = "select distinct x,y,dx,dy,imageFilename from (Image natural join (Image_has_ROI natural join ROI)) where experiment_eid= '%s' and ROISerial='%s' and iid=%s group by x,y;"%(RoiProps['Experiment ID'],RoiProps['ROI Serial'],RoiProps['Image ID'])
		ans = query_gawa(query1)

		path = ans[0][4]
		#print path
		import GawaImage
		images = GawaImage.convertToGIF([path])
		ImagePath = images[0]

		ROIDict=[]
		for i in range(len(ans)):
        		ROIDict.append({'ID':"paul"+str(i),'xpos':ans[i][0],'ypos':ans[i][1],'dx':ans[i][2],'dy':ans[i][3],'identifier':str(i+1)})

                print_HTML_content_single_pre()
		printBody(ImagePath,ROIDict,RoiProps)
                print_HTML_content_single_post()
	
	else:
                print_HTML_content_pre()
                print_browse_by_form()
                print_HTML_content_mid()	
                print_HTML_content_post()	
		

#print ending html
print_HTML_tail()

#close connection to DB
close_db(cursor, connection)
