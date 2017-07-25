var selectedKey=''
var subscribeSiteSet=new Set();
var unSubscribeSiteSet=new Set();
var sitesMap=new HashTable(3);
sitesMap.add(1,"site 1");
sitesMap.add(1,"site 2");
sitesMap.add(1,"site 3");
$(document).ready(function(){
	
	addBtnEvents();
	//add event on edit button for selected item
	$("button.edit-keyword").click(function (event) {
		$("div#edit-modal").modal('hide');
		var newKeyword=$("input.edit-keyword").val();
		editUrl='/edit-keyword/'+newKeyword+'/'+selectedKey+'/';
		$.ajax({
            type: 'PUT', // define the type of HTTP verb we want to use
            url: editUrl, // the url where we want to POST 
            encode: true,
            success: function (data, textStatus, jqXHR) {
                console.log("submit Successfully");
                $("div.alert").removeClass("alert-danger");
                $("div.alert").addClass("alert-success");
                $("p.messageFeedback").text("Edit successfull");
                closeAlert();
                fetchAllKeywords();
            },
            error: function (response, request) {
            	$("div.alert").removeClass("alert-success");
            	$("div.alert").addClass("alert-danger");
                var parsed_data = response.responseText;
                $("p.messageFeedback").text(parsed_data);
                closeAlert();
            }

        });
		
		
	});
	
	//add event on delete button for selected item
	$("button.delete-keyword").click(function (event) {
		$("div#delete-modal").modal('hide');
		var delUrl='/delete-keyword/'+selectedKey+'/';
		$.ajax({
            type: 'DELETE', // define the type of HTTP verb we want to use 
            url: delUrl, // the url where we want to POST 
            encode: true,
            success: function (data, textStatus, jqXHR) {
                console.log("submit Successfully");
                $("div.alert").removeClass("alert-danger");
                $("div.alert").addClass("alert-success");
                $("p.messageFeedback").text("Delete successfully");
                closeAlert();
                fetchAllKeywords();
            },
            error: function (response, request) {
            	$("div.alert").removeClass("alert-success");
            	$("div.alert").addClass("alert-danger");
                var parsed_data = response.responseText;
                $("p.messageFeedback").text(parsed_data);
                closeAlert();
            }

        });
	});
	
	//add event on add button for new item
	$("button.save-keyword").click(function (event) {
		$("div#new-keyword-modal").modal('hide');
		var newKeyword=$("input#new-keyword").val();
		var formData = {
            "keyword":newKeyword
        };
		
		$.ajax({
            type: 'POST', // define the type of HTTP verb we want to use 
            url: '/add-keyword/', // the url where we want to POST 
            data: formData, // our data object
            encode: true,
            success: function (data, textStatus, jqXHR) {
                console.log("submit Successfully");
                $("div.alert").addClass("alert-success");
                $("p.messageFeedback").text("Created successfully");
                closeAlert();
                fetchAllKeywords();
            },
            error: function (response, request) {
            	$("div.alert").removeClass("alert-success");
            	$("div.alert").addClass("alert-danger");
                var parsed_data = response.responseText;
                $("p.messageFeedback").text(parsed_data);
                closeAlert();
            }

        });
		
		
	});
	
	//add event to list of subscribe site.
	$(".subscribed-sites").click(function (event) {
		$(event.target).toggleClass("select-item");
		$(event.target).toggleClass("item-list"); 
		if(unSubscribeSiteSet.contains(event.target.id)) set.remove(event.target.id);
		else unSubscribeSiteSet.add(event.target.id);
	});

	
	//add event to list of unsubscribe site.
	$(".nonsubscribed-sites").click(function (event) {
		$(event.target).toggleClass("select-item");
		$(event.target).toggleClass("item-list"); 
		if(subscribeSiteSet.contains(event.target.id)){
				
				subscribeSiteSet.remove(event.target.id);
		}else {
			
			subscribeSiteSet.add(event.target.id);
			
		}
		subscribeSiteSet.print();
		//sitesMap.print();
	});
	
	//add event to subscribe btn to add selected sites to subscription side
	$(".subscribe-btn").click(function (event) {
		var siteName=sitesMap.search(event.target.id);
		$("subscribed-sites").append("<li>"+siteName+"</li>");
		if(unSubscribeSiteSet.contains(event.target.id)) set.remove(event.target.id);
		else unSubscribeSiteSet.add(event.target.id);
	});


});

// add events for edit and delete buttons from the subscriptions table
function addBtnEvents(){
	 $("button.keyword").click(function (event) {
	    	console.log("Clicked id "+event.target.id);
	    	selectedKey=event.target.id;
	    	var keywordEl='td#'+selectedKey+'-keyword';
	    	console.log("keyword selector"+keywordEl)
	    	$('input.edit-keyword').val($(keywordEl).html());
	    	$('label.delete-keyword').html($(keywordEl).html());
	    	
	    });
	
}


function fetchAllKeywords(){
	
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/getAllKeywords/', // the url where we want to POST
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            $('table#contentItems').find("tr:gt(0)").remove();
            console.log("the status gotten: " + textStatus);
            populateContentTable(data);
        },
        error: function (data, textStatus, jqXHR) {

            $('table#contentItems').find("tr:gt(0)").remove();
            $('table#contentItems').append("<tr style='width: 100%;'><td colspan=7 style='color:red;text-align: center;'>" + data.responseText + "</td></tr>");

        }

    });
	
}



/*populates html table with content if any from sever*/
function populateContentTable(data) {
	
	for(var i in data){
  	  console.log(i); // alerts key
  	console.log(data[i]); //alerts key's value
  	  var trHTML;
  	trHTML +='<tr><td id=\''+i+'-keyword\'>' + data[i] + '</td>'
  	+	'<td><button type="button" id=\''+i+'\' class="btn btn-info keyword" data-toggle="modal" style="margin-right:4px;" data-target=".edit-modal">'
	+	'<i class="fa fa-pencil" aria-hidden="true"></i>'
	+'</button>'

	+'<button type="button" id=\''+i+'\'	class="btn btn-primary keyword" data-toggle="modal" data-target=".delete-modal">'
		+'<i class="fa fa-trash" aria-hidden="true"></i>'
	+'</button></td></tr>'
  	  
  	}
	$('table#contentItems').append(trHTML);
	addBtnEvents();
}



function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(500, function () {
    $("#alerter").slideUp(500);
    });
}