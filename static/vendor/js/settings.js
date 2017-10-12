/**
 *  Settings js for the settings page
 */


$(document).ready(function(){
	fetchAllSettings();
//	addBtnEvents();
   
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
	console.log("is array: "+ Array.isArray(data[2]));
	console.log("The data: "+data[2]);
	for(var key in data){
  	  
		var setting=data[key];
	  	var trHTML ='<ul class="listing"><li><label style="font-weight: normal;">'+setting[11]+'</label></li><li ">'
									+	'<button type="button" id="'+setting[0]+'" class="btn btn-info keyword"'
									+		'data-toggle="modal" data-target=".edit-modal">'
									+	'<i class="fa fa-sliders" aria-hidden="true"></i>'
										'</button>'
							+		'</li>'
							+	'</ul>'
							+	'<div style="display: none;">'
							+	'	<p>We are here, right</p>'
							+	'</div>';
  	}
	$('div.keywords-list-sec').append(trHTML);
	//addBtnEvents();
}

function addBtnEvents(){
	 $("button.name").click(function (event) {
	    	console.log("Clicked id "+event.target.id);
	    	selectedKey=event.target.id;
	    	var nameEl='td#'+selectedKey+'-name';
	    	console.log("name selector"+nameEl)
	    	$('input.edit-name').val($(nameEl).html());
	    
	    });
	
}



function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(500, function () {
    $("#alerter").slideUp(500);
    });
}

