/**
 *  Settings js for the settings page
 */

var settingData=null;

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
	$(".load-settings-spinner").css("display","block");
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use 
        url: '/get-settings/', // the url where we want to POST 
        dataType: 'json', // our data object
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	settingData=data;
        	
        	for(var key in data){
        		var setting=data[key];
        		if(setting[14]!=undefined || setting[14]!=null){  //choose random subscriber to be default in settings listing
        			populateSettingTableTag(setting[14],data);
        			break;
        		}
        	}
        	
        },
        error: function (response, request) {
        	console.log("error occured fetching settings");
        }
    });
	
}


/*populates html table with content if any from sever*/
function populateTableContent(setting) {
			var noOfPages='<div class="col-sm-4  col-sm-offset-2  setting-label"><label>No of pages: </label></div>'
			+'<div style="margin-bottom: 4px;" class="col-sm-5">'
				+'<div class="input-group pages-number-spinner-'+setting[0]+'">'
					+'<span class="input-group-btn">'
						+'<button class="btn btn-default" data-dir="dwn"><span class="glyphicon glyphicon-minus"></span></button>'
					+'</span>'
					+'<input type="text"  disabled class="form-control text-center spinner-input"  value="1">'
					+'<span class="input-group-btn" style="float:left;">'
						+'<button class="btn btn-default"  data-dir="up"><span class="glyphicon glyphicon-plus"></span></button>'
					+'</span>'
				+'</div>'
			+'</div>'
			
		var minimumAlerts='<div class="col-sm-4  col-sm-offset-2 setting-label" style="clear: left;"><label>Minimum Jobs alerts: </label></div>'
		+'<div style="margin-bottom: 4px;" class="col-sm-5">'
			+'<div class="input-group alerts-number-spinner-'+setting[0]+'">'
				+'<span class="input-group-btn">'
					+'<button class="btn btn-default" data-dir="dwn"><span class="glyphicon glyphicon-minus"></span></button>'
				+'</span>'
				+'<input type="text" disabled class="form-control text-center  spinner-input" value="1">'
				+'<span class="input-group-btn" style="float:left;">'
					+'<button class="btn btn-default" data-dir="up"><span class="glyphicon glyphicon-plus"></span></button>'
				+'</span>'
			+'</div>'
		+'</div>'			
		
		var controlButtons='<div style="clear: left;" class="col-sm-12 text-center">'
			+	'<button type="button" id="'+setting[0]+'-edit" class="btn btn-success  setting-btn"'
			+		'data-toggle="modal" data-target=".edit-modal">'
			+	'<i class="fa fa-pencil" aria-hidden="true"></i> Save'
			+	'</button>'
			
			+	'<button type="button" class="btn btn-warning  setting-btn"'
			+		'data-toggle="modal" data-target=".edit-modal">'
			+	'<i class="fa fa-stop" aria-hidden="true"></i> Cancel'
			+	'</button>'
			
			
			+'</div>'
		
		var trHTML ='<ul class="listing"><li><label style="font-weight: normal;">'+setting[13]+'</label></li><li>'
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
		
	  	$('div.keywords-list-sec').append(trHTML);	
	  	
}


function populateSettingTableTag(id,data){
	var subscriberIdsAddedToSelectTag=new Set();
	$('div.keywords-list-sec').find("ul:gt(0)").remove();
	
	for(var key in data){
		var setting=data[key];
		
		subscriberIdsAddedToSelectTag.print();
		console.log(setting[14]);
		if(setting[14]==id){
			if(!subscriberIdsAddedToSelectTag.contains(setting[14])){
				populateSelectTag(setting,true);
				subscriberIdsAddedToSelectTag.contains(setting[14]);
			}
			subscriberIdsAddedToSelectTag.add(setting[14]);
			populateTableContent(setting);		
			setValuesToSubAddButtonsSettingsMenu(setting);
			
		}else{
			if(!subscriberIdsAddedToSelectTag.contains(setting[14])){
				populateSelectTag(setting,false);
				subscriberIdsAddedToSelectTag.contains(setting[14]);
			}
			subscriberIdsAddedToSelectTag.add(setting[14]);
			
		}
		
	}
	addClickEventToKeywordSettingBtn();
}


function populateSelectTag(setting,isDefault){
	console.log("We are coming three");
	if(isDefault){

		$('select#subscriber-sel').append('<option selected value='+setting[14]+'>'+setting[15]+'</option>');
		$('select#site-sel').append('<option selected value='+setting[6]+'>'+setting[7]+'</option>');
	}else{
		$('select#subscriber-sel').append('<option value='+setting[14]+'>'+setting[15]+'</option>');
		$('select#site-sel').append('<option value='+setting[6]+'>'+setting[7]+'</option>');
	}
			
}


function setValuesToSubAddButtonsSettingsMenu(setting){
	//setting[3] <-- this is no of pages per keyword
  	//setting[10] <-- per site

  	//add events to scrap page limit and maximum jobs to alert increment $ decrement buttons 
  	if(setting[3]===undefined  || setting[3]===null || String(setting[3]).trim()===''){
  		addClickEventToKeywordSubSettingPagesBtn(setting[10],setting[0]);
  	}else {
  		addClickEventToKeywordSubSettingPagesBtn(setting[3],setting[0]);
  	}
  	

  	if(setting[5]===undefined  || setting[5]===null || String(setting[5]).trim()===''){
  		addClickEventToKeywordSubSettingAlertsBtn(setting[11],setting[0]);
  	}else {
  		addClickEventToKeywordSubSettingAlertsBtn(setting[5],setting[0]);
  	}
  	
}


function addClickEventToKeywordSubSettingPagesBtn(maximunPageNo,id){

	$(document).on('click', '.pages-number-spinner-'+id+' button', function () {

		var btn = $(this),
			oldValue = btn.closest('.pages-number-spinner-'+id+'').find('input').val().trim(), //get current value in input box
			newVal = 1;
		
		if (btn.attr('data-dir') == 'up') {
			if(oldValue==maximunPageNo){
				newVal=maximunPageNo;
			}else if(oldValue>maximunPageNo){
				oldValue=maximunPageNo;
			}else newVal = parseInt(oldValue) + 1;
		} else {
			if (oldValue > 1) {
				newVal = parseInt(oldValue) - 1;
			} else {
				newVal = 1;
			}
		}
		btn.closest('.pages-number-spinner-'+id+'').find('input').val(newVal);
	});
	
}


function addClickEventToKeywordSubSettingAlertsBtn(minimuJobsAlert,id){
	$(document).on('click', '.alerts-number-spinner-'+id+' button', function () {    
		var btn = $(this),
			oldValue = btn.closest('.alerts-number-spinner-'+id+'').find('input').val().trim(), //get current value in input box
			newVal = 1;
		
		if (btn.attr('data-dir') == 'up') {
			if(oldValue==minimuJobsAlert){
				newVal=minimuJobsAlert;
			}else if(oldValue>minimuJobsAlert){
				oldValue=minimuJobsAlert;
			}else newVal = parseInt(oldValue) + 1;
		} else {
			if (oldValue > 1) {
				newVal = parseInt(oldValue) - 1;
			} else {
				newVal = 1;
			}
		}
		btn.closest('.alerts-number-spinner-'+id+'').find('input').val(newVal);
	});
	
	$(".load-settings-spinner").css("display","none");
}


function addClickEventToKeywordSettingBtn(){
	
	 $("button.setting-btn").click(function (event) {
		    
	    	var selectedKey=event.target.id;
	    	var settingPanel='div#'+selectedKey+'-panel';
	    	//$(settingPanel).val($(nameEl).html());
	    	$(settingPanel).toggle();
	    });	
	 
	 
}


function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(500, function () {
    $("#alerter").slideUp(500);
    });
}

