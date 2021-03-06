/**
 *  Settings js for the settings page
 */

var settingData=null;
var currentSelectedSubscriber=null;
var currentSelectedSite=null;
var count=0;

$(document).ready(function(){
	fetchAllSettings();
});



//Fetch all subscriptions and store on cache:
function fetchAllSettings(){
	$(".load-settings-spinner").css("display","block");
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use 
        url: '/get-settings/', // the url where we want to POST 
        dataType: 'json', // our data object
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	settingData=data;
        	for(var x=0;x<data.length;x++){
        		var setting=data[x];
        		if(setting[14]!=undefined || setting[14]!=null){  //choose random subscriber to be default in settings listing
        			currentSelectedSite=setting[1];
        			currentSelectedSubscriber=setting[14];
        			populateSettingTableTag(setting[14],setting[1],data);
        			break;
        		}
        	}
        	
        },
        error: function (response, request) {
        }
    });
	
}


function populateSettingTableTag(subscriberId,siteId,data){
	var keywordIdsAlreadyAddedInListing=new Set();
	$('div.keywords-list-sec').find("ul:gt(0)").remove();
	$('div.keywords-list-sec').find("div:gt(0)").remove();
	$('#subscriber-sel').find("option:gt(0)").remove();
	$('#site-sel').find("option:gt(0)").remove();
	
	for(var x=0; x<data.length;x++){
		
		var setting=data[x];

		if(setting[14]==subscriberId){
			populateSubscriberSelectTag(setting,true);
		}else{
			populateSubscriberSelectTag(setting,false);
		}
		
		//populate sited to select tag.
		if(setting[1]==siteId){
			populateSiteSelectTag(setting,true);
		}else{
			populateSiteSelectTag(setting,false);
		}
		
		//make kewords listing
		if(!keywordIdsAlreadyAddedInListing.contains(setting[12]) &&  setting[14]==subscriberId && setting[1]==siteId){
			populateTableContent(setting);
			setValuesToSubAddButtonsSettingsMenu(setting);
			keywordIdsAlreadyAddedInListing.add(setting[12]);
		}
		
	}

	addClickEventToKeywordSettingBtn();
	addClickEventToCancelKeywordSettingBtn()
}


function populateSubscriberSelectTag (setting,isDefault){
	$('select#subscriber-sel option#subscriber-'+setting[14]+'').remove();
	if(isDefault){
		$('select#subscriber-sel').append('<option id=subscriber-'+setting[14]+' selected value='+setting[14]+'>'+setting[15]+'</option>');
	}else{
		$('select#subscriber-sel').append('<option id=subscriber-'+setting[14]+' value='+setting[14]+'>'+setting[15]+'</option>');
		
	}
			
}


function populateSiteSelectTag(setting,isDefault){
	$('select#site-sel option#site-'+setting[6]+'').remove();
	if(isDefault){
		$('select#site-sel').append('<option id=site-'+setting[6]+' selected value='+setting[6]+'>'+setting[7]+'</option>');
	}else{
		$('select#site-sel').append('<option id=site-'+setting[6]+' value='+setting[6]+'>'+setting[7]+'</option>');
		
	}
	
}


function setValuesToSubAddButtonsSettingsMenu(setting){
	//setting[3] <-- this is no of pages per keyword
  	//setting[10] <-- per site
  	//add events to scrap page limit and maximum jobs to alert increment $ decrement buttons 
  	var id=setting[0]+'-'+setting[1]+'-'+setting[2];
  		addClickEventToKeywordSubSettingPagesBtn(setting[3],id);  
  		addClickEventToKeywordSubSettingAlertsBtn(setting[5],id);
  		addClickEventToKeywordSettingSaveBtn(id);
  		
}


function addClickEventToKeywordSubSettingPagesBtn(maximunPageNo,id){

	$( '.pages-number-spinner-'+id+' button').on('click',function () {

		var btn = $(this);
		var oldValue = btn.closest('.pages-number-spinner-'+id+'').find('input').val().trim(); //get current value in input box
		var newVal = 1;
		
		if (btn.attr('data-dir') == 'up') {
			newVal = parseInt(oldValue) + 1;
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
	$('.alerts-number-spinner-'+id+' button').on('click', function () {  
		var btn = $(this);
		var oldValue = btn.closest('.alerts-number-spinner-'+id+'').find('input').val().trim(); //get current value in input box
		var newVal = 1;
		
		if (btn.attr('data-dir') == 'up') {
			newVal = parseInt(oldValue) + 1;
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


function addClickEventToKeywordSettingSaveBtn(id){
	$(document).on('click', '#'+id+'-save', function () {  
		$(".settings-status-spinner-"+id).css("display","block");
		var btn = $(this),
			noOfJobsAlerts = parseInt($('.alerts-number-spinner-'+id+'').find('input').val().trim()); //get current value in input box
			noOfPages = parseInt($('.pages-number-spinner-'+id+'').find('input').val().trim()); //get current value in input box
			var idArr=id.split("-");
			subscriberId=idArr[0];
			siteId=idArr[1];
			keywordId=idArr[2];
			
			var formData = {
		            "subscriberId": subscriberId,
		            "siteId": siteId,
		            "keywordId": keywordId,
		            "minimumAlert": noOfJobsAlerts,
		            "pageLimit": noOfPages
		        };
			$.ajax({
		        type: 'PUT', // define the type of HTTP verb we want to use 
		        url: '/update-setting/ ', // the url where we want to POST 
		        dataType: 'json', // our data object
		        data: formData, // our data object
	            encode: true,
		        success: function (data, textStatus, jqXHR) {
		        	settingData=data;
		        	$(".settings-status-spinner-"+id).css("display","none");
		        },
		        error: function (response, request) {
		        	$(".settings-status-spinner-"+id).css("display","none");
		        }
		    });
			
	});
	
}

function addClickEventToKeywordSettingBtn(){ 
	
	 $("button.setting-btn").click(function (event) {
		    
	    	var selectedKey=event.target.id;
	    	var settingPanel='div#'+selectedKey+'-panel';
	    	//$(settingPanel).val($(nameEl).html());
	    	$(settingPanel).toggle();
	    });	
}


function addClickEventToCancelKeywordSettingBtn(){
	
	 $("button.setting-cancel-btn").click(function (event) {
		    idArr=event.target.id.split("-");
	    	var selectedKey=idArr[0]+"-"+idArr[1]+"-"+idArr[2];
	    	var settingPanel='div#'+selectedKey+'-panel';
	    	//$(settingPanel).val($(nameEl).html());
	    	$(settingPanel).toggle();
	    });	
}


/*populates html table with content if any from sever*/
function populateTableContent(setting) {
			var noOfPages='<div class="col-sm-4  col-sm-offset-2  setting-label"><label>No of pages: </label></div>'
			+'<div style="margin-bottom: 4px;" class="col-sm-5">'
				+'<div class="input-group pages-number-spinner-'+setting[0]+'-'+setting[1]+'-'+setting[2]+'">'
					+'<span class="input-group-btn">'
						+'<button class="btn btn-default" data-dir="dwn"><span class="glyphicon glyphicon-minus"></span></button>'
					+'</span>'
					+'<input type="text"  disabled class="form-control text-center spinner-input"  value="'+setting[3]+'">'
					+'<span class="input-group-btn" style="float:left;">'
						+'<button class="btn btn-default"  data-dir="up"><span class="glyphicon glyphicon-plus"></span></button>'
					+'</span>'
				+'</div>'
			+'</div>'
			
		var minimumAlerts='<div class="col-sm-4  col-sm-offset-2 setting-label" style="clear: left;"><label>Minimum Jobs alerts: </label></div>'
		+'<div style="margin-bottom: 4px;" class="col-sm-5">'
			+'<div class="input-group alerts-number-spinner-'+setting[0]+'-'+setting[1]+'-'+setting[2]+'">'
				+'<span class="input-group-btn">'
					+'<button class="btn btn-default" data-dir="dwn"><span class="glyphicon glyphicon-minus"></span></button>'
				+'</span>'
				+'<input type="text" disabled class="form-control text-center  spinner-input" value="'+setting[4]+'">'
				+'<span class="input-group-btn" style="float:left;">'
					+'<button class="btn btn-default" data-dir="up"><span class="glyphicon glyphicon-plus"></span></button>'
				+'</span>'
			+'</div>'
		+'</div>'			
		
		var controlButtons='<div style="clear: left;" class="col-sm-12 text-center">'
			+	'<button type="button" id="'+setting[0]+'-'+setting[1]+'-'+setting[2]+'-save" class="btn btn-success  setting-btn"'
			+		'data-toggle="modal" data-target=".edit-modal">'
			+	'<i class="fa fa-pencil" aria-hidden="true"></i> Save'
			+	'</button>'
			
			+	'<button type="button" id="'+setting[0]+'-'+setting[1]+'-'+setting[2]+'-cancel" class="btn btn-warning  setting-btn setting-cancel-btn"'
			+		'data-toggle="modal" data-target=".edit-modal">'
			+	'<i class="fa fa-stop" aria-hidden="true"></i> Cancel'
			+	'</button>'
			+'</div>'
			+'<div style="display: none" class="col-sm-12  text-center settings-status-spinner-'+setting[0]+'-'+setting[1]+'-'+setting[2]+'">'
			+'		<p>'
			+'		<span>Loading settings </span>'
			+'		<i class="fa fa-refresh fa-spin fa-1x fa-fw"></i>'
			+'	</p>'
			+'</div>'
		
		var trHTML ='<ul class="listing"><li><label style="font-weight: normal;">'+setting[13]+'</label></li><li>'
									+	'<button type="button" id="'+setting[0]+'-'+setting[1]+'-'+setting[2]+'" class="btn btn-info setting-btn"'
									+		'data-toggle="modal" data-target=".edit-modal">'
									+	'<i class="fa fa-sliders" aria-hidden="true"></i>'
									+	'</button>'
							+		'</li>'
							+	'</ul>'
							+	'<div id='+setting[0]+'-'+setting[1]+'-'+setting[2]+'-panel class="container-fluid" style="display: none" >'
							+	'<div class="row setting-panel text-center">'
								+	noOfPages
								+	minimumAlerts
								+	controlButtons
							+	'</div>'
							+	'</div>';
		
	  	$('div.keywords-list-sec').append(trHTML);	
	  	
}



$('#site-sel').on('change', function(event) {
	currentSelectedSite=this.value;
	populateSettingTableTag(currentSelectedSubscriber,this.value,settingData);
	
}); 


$('#subscriber-sel').on('change', function(event) {
	currentSelectedSubscriber=this.value;
	populateSettingTableTag(this.value,currentSelectedSite,settingData);
}); 



function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(500, function () {
    $("#alerter").slideUp(500);
    });
}


