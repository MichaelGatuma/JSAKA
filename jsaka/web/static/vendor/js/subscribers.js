var selectedSubscriptionKey
var subscribeSiteSet=new Set();
var unSubscribeSiteSet=new Set();
var sitesMap=new HashTable(3);


var subscribeKeywordSet=new Set();
var unsubscribeKeywordSet=new Set();
var keywordsMap=new HashTable(3);

var finalSubscribedKeywords=new Set();
var finalSubscribedSites=new Set();

var siteKeywordMap=new HashTable(3);



$(document).ready(function(){

	fetchAllSites();
	fetchAllKeywords();
	
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
	$("button.delete-subscription").click(function (event) {
		$("div#delete-modal").modal('hide');
		var delUrl='/delete-subscription/'+selectedSubscriptionKey+'/';
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
                location.reload();
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
	$(".nonsubscribed-sites").click(function (event) {
		$(event.target).toggleClass("select-item");
		$(event.target).toggleClass("item-list"); 
		var bool=$("#"+event.target.id).hasClass("select-item");
		if(bool) subscribeSiteSet.add(event.target.id);
		else subscribeSiteSet.remove(event.target.id);
		subscribeSiteSet.print();
	});

	
	//add event to list of unsubscribe site.
	$(".subscribed-sites").click(function (event) {
		$(event.target).toggleClass("select-item");
		$(event.target).toggleClass("item-list"); 
		
		var bool=$("#"+event.target.id).hasClass("select-item");
		if(bool) unSubscribeSiteSet.add(event.target.id);
		else unSubscribeSiteSet.remove(event.target.id);
		hideShowKeywordSection();
		
	});
	
	//add event to subscribe btn to add selected sites to subscription list
	$(".site-subscribe-btn").click(function (event) {
		
		jQuery.each(subscribeSiteSet.values,function(index, value){
			var siteName=sitesMap.search(value);
			$(".subscribed-sites").append("<li id="+value+">"+siteName+"</li>");
			$(".nonsubscribed-sites li#"+value).remove();
			unSubscribeSiteSet.remove(value);
			
		});
		hideShowKeywordSection();
	});

	
	//add event to unsubscribe btn to remove selected sites from subscription list
	$(".site-unsubscribe-btn").click(function (event) {
		jQuery.each(unSubscribeSiteSet.values,function(index, value){
			var siteName=sitesMap.search(value);
			$(".subscribed-sites li#"+value).remove();
			$(".nonsubscribed-sites").append("<li id="+value+">"+siteName+"</li>");
			
			
			subscribeSiteSet.remove(value);
		});
		hideShowKeywordSection();
	});
	
	

	
	//add event to list of nonsubscribe keywords list.
	$(".nonsubscribed-keywords").click(function (event) {
		$(event.target).toggleClass("select-item");
		$(event.target).toggleClass("item-list"); 
		var bool=$(event.target).hasClass("select-item");
		if(bool) subscribeKeywordSet.add(event.target.id);
		else unsubscribeKeywordSet.remove(event.target.id);
		
	});

	
	//add event to list of unsubscribe site.
	$(".subscribed-keywords").click(function (event) {
		$(event.target).toggleClass("select-item");
		$(event.target).toggleClass("item-list"); 
		var bool=$(event.target).hasClass("select-item");
		if(bool) unsubscribeKeywordSet.add(event.target.id);
		else subscribeKeywordSet.remove(event.target.id);
		
	});
	
	//add event to subscribe btn to add selected sites to subscription list
	$(".keyword-subscribe-btn").click(function (event) {
		subscribeKeywordSet.print();
		jQuery.each(subscribeKeywordSet.values,function(index, value){
			var keywordName=keywordsMap.search(value);
			$(".nonsubscribed-keywords #"+value).remove();
			$(".subscribed-keywords").append("<li id="+value+">"+keywordName+"</li>");
			unsubscribeKeywordSet.remove(value);
		});
	});

	
	//add event to unsubscribe btn to remove selected keyword(s) from subscription list
	$(".keyword-unsubscribe-btn").click(function (event) {
		jQuery.each(unsubscribeKeywordSet.values,function(index, value){
			var keywordName=keywordsMap.search(value);
			$(".subscribed-keywords li#"+value).remove();
			$(".nonsubscribed-keywords").append("<li id="+value+">"+keywordName+"</li>");
			subscribeKeywordSet.remove(value);
		});
		
	});

	
	$(".new-subsription-btn").click(function (event) {
		
		var style=$("#site-keyword").css("display");
		if(style!=='none') {
			console.log("here one");
			$("#site-keyword").css("display","none");
			console.log(subscribeKeywordSet.values);
			var keywordsToSend=new Set(3);
			jQuery.each(subscribeKeywordSet.values,function(index, value){
				var keyWrd=value.substring(value.indexOf('-')+1,value.indexOf('-')+2);
				keywordsToSend.add(keyWrd);
			});
			
			var sitesToSend=new Set(3);
			jQuery.each(subscribeSiteSet.values,function(index, value){
				var siteToSnd=value.substring(value.indexOf('-')+1,value.indexOf('-')+2);
				sitesToSend.add(siteToSnd);
			});
			
			var email=$("#subscriber-email").val();
			console.log("email "+ email);
			sitesS=JSON.stringify(sitesToSend.values);
			keywordS=JSON.stringify(keywordsToSend.values);
			
			var formData = {
		            "email": email,
		            "sites": sitesS,
		            "keywords": keywordS
		        };
			console.log("Form data "+formData)
			$.ajax({
	            type: 'POST', // define the type of HTTP verb we want to use 
	            url: '/add-subscriber/', // the url where we want to POST 
	            data: formData, // our data object
	            encode: true,
	            success: function (data, textStatus, jqXHR) {
	                console.log("submit new sub Successfully");
	                $("div.alert").addClass("alert-success");
	                $("p.messageFeedback").text("Created successfully");
	                closeAlert();
	                location.reload();
	            },
	            error: function (response, request) {
	            	$("div.alert").removeClass("alert-success");
	            	$("div.alert").addClass("alert-danger");
	                var parsed_data = response.responseText;
	                $("p.messageFeedback").text(parsed_data);
	                closeAlert();
	            }

	        });
			
			$(".new-subsription-btn").html("<i class='fa fa-plus-circle' aria-hidden='true'></i>  New subscription");
		}else {
			console.log("here two");
			$("#site-keyword").css("display","block");
			$(".new-subsription-btn").html("<i class='fa fa-plus-circle' aria-hidden='true'></i>  Save subscription");
			
		}
	});

	
});



// hide keywords section is no site is selected

function hideShowKeywordSection(){
	
	if(subscribeSiteSet.length()!=0){
		$(".keywordSection").css("display","");
	}else{
		
		var ids=$(".subscribed-keywords li").get();
		for(x=0;x<ids.length;x++){
			var id=$(ids[x]).attr('id');
			var keywordName=keywordsMap.search(id);
			$(".nonsubscribed-keywords").append("<li id="+id+">"+keywordName+"</li>");
			$(".subscribed-keywords #"+id).remove();
			
		}
		
		ids=$(".nonsubscribed-keywords li.select-item").get();
		for(x=0;x<ids.length;x++){
			var id=$(ids[x]).attr('id');
			subscribeKeywordSet.remove(id);
		}
		
		$(".nonsubscribed-keywords li").removeClass("select-item");
		$(".nonsubscribed-keywords li").removeClass("item-list");
		$(".keywordSection").css("display","none");
	    $(".keywordSection").fadeTo(300, 500).slideUp(500, function () {
	    $(".keywordSection").slideUp(500);
	    });
	}
}


// add events for edit and delete buttons from the subscriptions table
function addBtnEvents(){
	 
	 $("button.subscription").click(function (event) {
	    	
		    selectedSubscriptionKey=$(event.target).parent().parent().attr('id');
	    	var isDelete=$(event.target).hasClass("delete-sub");
	    	var isEdit=$(event.target).hasClass("edit-sub");
	  
	    	if(isEdit){
	    
	    	}else if(isDelete){
	    		console.log("tr#"+selectedSubscriptionKey+" td");
	    		elemnt="tr#"+selectedSubscriptionKey+" td";
	    		var subMail=$(elemnt).html();
	    		console.log("mail "+subMail);
	    		$("label.delete-subscription").html(subMail);
	    	}else{
	    		
	    	}
	    	
	    });
}




function fetchAllKeywords(){
	
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/getAllKeywords/', // the url where we want to POST
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	for(var i in data){
        		keywordsMap.add('keyword-'+i,data[i]);
        		
        		$(".nonsubscribed-keywords").append("<li id=keyword-"+i+">"+data[i]+"</li>");
        	}
        },
        error: function (data, textStatus, jqXHR) {

        	 $(".nonsubscribed-keywords").append("<li>We faced problems while loading available keywords. Kindly reload page</li>");

        }

    });
	
}

function fetchAllSites(){

	console.log("Fetching sites");
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/getAllSites/', // the url where we want to POST
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	console.log(data);
        	for(var i in data){
        		sitesMap.add('site-'+i,data[i]);
        		$(".nonsubscribed-sites").append("<li id=site-"+i+">"+data[i]+"</li>");
        	}

        },
        error: function (data, textStatus, jqXHR) {

        	 $(".nonsubscribed-sites").append("<li>We faced problems while loading available sites. Kindly reload page</li>");

        }

    });
	
}

function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(50, function () {
    $("#alerter").slideUp(50);
    });
}
