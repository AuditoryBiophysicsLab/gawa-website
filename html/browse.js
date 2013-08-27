$(document).ready(function(){

	function drawTable() {
		
		//filter options
		var filterData = $('#form_options').serialize();
		//field display options
		var checkBoxData = $('#check_box_data').serialize();	
		var allData = filterData + '&' + checkBoxData;
		$(".ajax-destroyable").remove();
		$("#maincontent_inner").append('<img class = "loadGif" src = "http://bioed.bu.edu/students_13/gawa/images/thinking.gif"/>');	
		var request = $.ajax({
			url: "http://bioed.bu.edu/cgi-bin/students_13/gawa/ajax.py",
			type: "post",
			data: allData	
		});

		request.done(function (response, textStatus, jqXHR){
			$('.loadGif').remove();
			$('#results').append(response); //append to table
			hideFields(checkBoxData);				
		});
		
	}
	
	function hideFields(checkBoxData){
		$('.checkbox').each(function(){	
			if (checkBoxData.indexOf($(this).attr('id')) == -1){
				$('.' + $(this).attr('id')).hide();
			}
		});
	}
					
		

	function drawOptions(){
			
		var stringData = $('#form_browse_by').serialize();		
		$(".ajax-destroyable").remove();
		$(".ajax-destroyable-options").remove();
		$("#maincontent_inner").append('<img class = "loadGif" src = "http://bioed.bu.edu/students_13/gawa/images/thinking.gif"/>');

		var request = $.ajax({
			url: "http://bioed.bu.edu/cgi-bin/students_13/gawa/ajax.py",
			type: "post",
			data: stringData	
		});

		request.done(function (response, textStatus, jqXHR){
			
			splitResponse = response.split('delimiter');
			
			$('#sidebar_inner').append(splitResponse[0]);
			$('#maincontent_inner').append(splitResponse[1]);
			$('.loadGif').remove();
			processCheckbox()	
		});
	}

	function processCheckbox(){
			
		$('.checkbox').each(function() {
			var id = this.id;
			$(this).click(function(){
				$('.' + id).toggle();
			});
					
		});

		$('.default-hide').hide();//navOptions arrows
		$('.default-show').show();

	


		$('#navOpen').click(function(){
			$('#checkboxes').toggle();
			$('.arrow').toggle();
		});
		
		$('#navOpen').mouseover(function(){
			$(this).css('cursor', 'pointer');		
			
		})
	}

	function drawFrequencies(eid, level) {
		cgiForm = 'drawFrequencies=yes&eid=' + eid + '&level=' + level;
		alert(cgiForm);
		$('#experiment_page_frequencies_ajax').empty()
		var request = $.ajax({
                        url: "http://bioed.bu.edu/cgi-bin/students_13/wrchapin/gawa/ajax.py",
                        type: "post",
                        data: cgiForm
                });

                request.done(function (response, textStatus, jqXHR){
                       $('#experiment_page_frequencies_ajax').append(response); 
                       $('#') 
                });
	
	
	
	}
	function drawImageInfo(eid, level, freq){
		cgiForm = 'drawImageInfo=yes&eid=' + eid + '&level=' + level + '&freq=' + freq;
                $('#experiment_page_image_info').empty()
                var request = $.ajax({
                        url: "http://bioed.bu.edu/cgi-bin/students_13/gawa/ajax.py",
                        type: "post",
                        data: cgiForm
                });

                request.done(function (response, textStatus, jqXHR){
                       $('#experiment_page_image_info').append(response); 
                });
	
	}			


	$(".drawOptionsOnChange").change(drawOptions);
	$(document).on('change', '.drawTableOnChange', drawTable);
	$('.experiment_page_level, .experiment_page_freq').click(function(){
	
		thisClass = $(this).attr('class').split(' ')[0];
		$('.' + thisClass).removeClass('selected');
		$(this).addClass('selected');
		eid = $(this).attr('class').split(' ')[1];
		//get selected freq and level, then query DB and display results!

		selectedLevel = $('.experiment_page_level.selected').attr('id');
		selectedFreq = $('.experiment_page_freq.selected').attr('id');
			
		if (selectedFreq != undefined && selectedLevel != undefined){
			drawImageInfo(eid, selectedLevel, selectedFreq);
		}
	})
	

});




