/**
 *  Settings js for the settings page
 */


$(document).ready(function(){
	fetchAllSettings();
		//url: 'updateContentById?contentId=' + contentId, 
	
//	$("button.edit-name").click(function (event) {
//		$("div#edit-modal").modal('hide');
//		var newname=$("input.edit-name").val();
//		editUrl='/edit-name/'+newname+'/'+selectedKey+'/';
//		$.ajax({
//            type: 'PUT', // define the type of HTTP verb we want to use
//            url: editUrl, // the url where we want to POST 
//            encode: true,
//            success: function (data, textStatus, jqXHR) {
//                console.log("submit Successfully");
//                $("div.alert").removeClass("alert-danger");
//                $("div.alert").addClass("alert-success");
//                $("p.messageFeedback").text("Edit successfull");
//                closeAlert();
//                fetchAllnames();
//            },
//            error: function (response, request) {
//            	$("div.alert").removeClass("alert-success");
//            	$("div.alert").addClass("alert-danger");
//                var parsed_data = response.responseText;
//                $("p.messageFeedback").text(parsed_data);
//                closeAlert();
//            }
//
//        });
//		
//		
//	});
	
	
	
});




//Fetch all subscriptions and store on cache:
function fetchAllSettings(){
	console.log("Fetching settings");
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use 
        url: '/get-settings/', // the url where we want to POST 
        dataType: 'json', // our data object
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	console.log('and the data is: '+data)
        	populateContentTable(data);
        },
        error: function (response, request) {
        	console.log("error occured fetching settings");
        }

    });
}


/*populates html table with content if any from sever*/
function populateContentTable(data) {
	$('div.keywords-list-sec').find("ul:gt(0)").remove();
	
	var siteSet=new Set();
	var subscriberSet= new Set();
	var trHTML='';

	
	var noOfPages='<div class="col-sm-4 setting-label"><label>No of pages: </label></div>'
					+'<div style="margin-bottom: 4px;" class="col-sm-8">'
						+'<div class="input-group number-spinner">'
							+'<span class="input-group-btn">'
								+'<button class="btn btn-default" data-dir="dwn"><span class="glyphicon glyphicon-minus"></span></button>'
							+'</span>'
							+'<input type="text" class="form-control text-center" value="1">'
							+'<span class="input-group-btn">'
								+'<button class="btn btn-default" data-dir="up"><span class="glyphicon glyphicon-plus"></span></button>'
							+'</span>'
						+'</div>'
					+'</div>'
					
	var minimumAlerts='<div class="col-sm-4 setting-label"><label>Minimum Jobs alerts: </label></div>'
		+'<div style="margin-bottom: 4px;" class="col-sm-8">'
			+'<div class="input-group number-spinner">'
				+'<span class="input-group-btn">'
					+'<button class="btn btn-default" data-dir="dwn"><span class="glyphicon glyphicon-minus"></span></button>'
				+'</span>'
				+'<input type="text" class="form-control text-center" value="1">'
				+'<span class="input-group-btn">'
					+'<button class="btn btn-default" data-dir="up"><span class="glyphicon glyphicon-plus"></span></button>'
				+'</span>'
			+'</div>'
		+'</div>'			

	
			
			
	for(var key in data){
		var setting=data[key];
		
		
		var controlButtons='<div class="text-center">'
			+	'<button type="button" id="'+setting[0]+'-edit" class="btn btn-info  setting-btn"'
			+		'data-toggle="modal" data-target=".edit-modal">'
			+	'<i class="fa fa-pencil" aria-hidden="true"></i> Edit'
			+	'</button>'
			
			+	'<button type="button" id="'+setting[0]+'-cancel" class="btn btn-info  setting-btn"'
			+		'data-toggle="modal" data-target=".edit-modal">'
			+	'<i class="fa fa-stop" aria-hidden="true"></i> Cancel'
			+	'</button>'
			
			
			+'</div>'
		
		
		
		
	    trHTML +='<ul class="listing"><li><label style="font-weight: normal;">'+setting[11]+'</label></li><li>'
									+	'<button type="button" id="'+setting[0]+'" class="btn btn-info setting-btn"'
									+		'data-toggle="modal" data-target=".edit-modal">'
									+	'<i class="fa fa-sliders" aria-hidden="true"></i>'
									+	'</button>'
							+		'</li>'
							+	'</ul>'
							+	'<div id='+setting[0]+'-panel class="container-fluid" style="display: none" >'
							+	'<div class="row setting-panel text-center">'
								+	noOfPages
								+	minimumAlerts
								+	controlButtons
							+	'</div>'
							+	'</div>';
	    siteSet.add(setting[7]);
	  	subscriberSet.add(setting[13]);	
	}

	jQuery.each(subscriberSet.values,function(index, value){
		$('select#subscriber-sel').append('<option>'+value+'</option>');
		$('select#site-sel').append('<option>'+siteSet.values[index]+'</option>');
	});
	
	$('div.keywords-list-sec').append(trHTML);
	addBtnEvents();
}


function addBtnEvents(){
	
	 $("button.setting-btn").click(function (event) {
		    
	    	var selectedKey=event.target.id;
	    	var settingPanel='div#'+selectedKey+'-panel';
	    	//$(settingPanel).val($(nameEl).html());
	    	$(settingPanel).toggle();
	    });	
	 
	 $(document).on('click', '.number-spinner button', function () {    
			var btn = $(this),
				oldValue = btn.closest('.number-spinner').find('input').val().trim(),
				newVal = 0;
			
			if (btn.attr('data-dir') == 'up') {
				newVal = parseInt(oldValue) + 1;
			} else {
				if (oldValue > 1) {
					newVal = parseInt(oldValue) - 1;
				} else {
					newVal = 1;
				}
			}
			btn.closest('.number-spinner').find('input').val(newVal);
		});
}


function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(500, function () {
    $("#alerter").slideUp(500);
    });
}

