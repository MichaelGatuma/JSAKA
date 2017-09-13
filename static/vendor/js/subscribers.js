var selectedSubscriptionKey

var sitesMap=new HashTable(3);
var allSubscriptions; //object
var allKeywords;
var allSites;

//these acts as placeholders for items during selection of sites and keywords to subscribe and unsubscribe before persistence
var subscribeSiteSet=new Set();
var unSubscribeSiteSet=new Set();
var subscribeKeywordSet=new Set();
var unsubscribeKeywordSet=new Set();

var keywordsMap=new HashTable(3);

var finalSubscribedKeywords=new Set();
var finalSubscribedSites=new Set();
//holds keywors each site is subscribed to
var siteKeywordMap=new HashTable(3);

//contains the current subscribed items in a set
var currentSubscribedSites=new Set();
var currentSubscribedKeywords=new Set();
var currentNonSubscribedSites=new Set();
var currentNonSubscribedKeywords=new Set();

$(document).ready(function(){

	fetchAllSites();
	fetchAllKeywords();
	fetchAllSubscriptions();
	
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
			if(!currentSubscribedSites.contains(value)){
				$(".subscribed-sites").append("<li id="+value+">"+siteName+"</li>");
				currentSubscribedSites.add(value);
				currentNonSubscribedSites.remove(value);
			}
			

			
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
			
			if(!currentNonSubscribedSites.contains(value)){
				$(".nonsubscribed-sites").append("<li id="+value+">"+siteName+"</li>");
				currentSubscribedSites.remove(value);
				currentNonSubscribedSites.add(value);
			}
			
			
			
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
			
			console.log(currentSubscribedKeywords.contains(value));
			if(!currentSubscribedKeywords.contains(value)){
				$(".subscribed-keywords").append("<li id="+value+">"+keywordName+"</li>");
				currentSubscribedKeywords.add(value);
				currentNonSubscribedKeywords.remove(value);
			}
					
			unsubscribeKeywordSet.remove(value);
		});
	});

	
	//add event to unsubscribe btn to remove selected keyword(s) from subscription list
	$(".keyword-unsubscribe-btn").click(function (event) {
		jQuery.each(unsubscribeKeywordSet.values,function(index, value){
			var keywordName=keywordsMap.search(value);
			$(".subscribed-keywords li#"+value).remove();
			
			console.log(currentNonSubscribedKeywords.contains(value));
			if(!currentNonSubscribedKeywords.contains(value)){
				$(".nonsubscribed-keywords").append("<li id="+value+">"+keywordName+"</li>");
				currentSubscribedKeywords.remove(value);
				currentNonSubscribedKeywords.add(value);
			}
			
			subscribeKeywordSet.remove(value);
		});
		
	});

	
	$(".new-subsription-btn").click(function (event) {
		
		var style=$("#site-keyword").css("display");
		var hasEditClass=$("#site-keyword").hasClass("edit");
		console.log("Display "+style);
		console.log("Has edit class "+hasEditClass);
		if(style!=='none' && !hasEditClass) {
			console.log("here one");
			$("#site-keyword").css("display","none");
			
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
			
			$.ajax({
	            type: 'POST', // define the type of HTTP verb we want to use 
	            url: '/add-subscriber/', // the url where we want to POST 
	            data: formData, // our data object
	            encode: true,
	            success: function (data, textStatus, jqXHR) {
	              
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
		}else if(style==='none' && !hasEditClass){
			
			$("#site-keyword").css("display","block");
			$(".new-subsription-btn").html("<i class='fa fa-plus-circle' aria-hidden='true'></i>  Save subscription");
			
		}else{
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
			
			$.ajax({
	            type: 'PUT', // define the type of HTTP verb we want to use 
	            url: '/update-subscriber/'+selectedSubscriptionKey, // the url where we want to POST 
	            data: formData, // our data object
	            encode: true,
	            success: function (data, textStatus, jqXHR) {
	              
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
		}
	});

	
});


//Fetch all subscriptions and store on cache:
function fetchAllSubscriptions(){
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use 
        url: '/getAllSubscribers/', // the url where we want to POST 
        dataType: 'json', // our data object
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	allSubscriptions=data;
        },
        error: function (response, request) {
        	console.log("error occured fetching subscriptions")
        }

    });
}


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
			currentSubscribedKeywords.remove(id);
			currentNonSubscribedKeywords.add(id);
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
	 
	 $("button.subscription-control").click(function (event) {
		    selectedSubscriptionKey=$(event.target).parent().parent().attr('id');
	    	var isDelete=$(event.target).hasClass("delete-sub");
	    	var isEdit=$(event.target).hasClass("edit-sub");
	  
	    	if(isEdit){
	    		$("#site-keyword").css("display","block");
	    		$("#site-keyword").addClass("edit");
	    		$(".new-subsription-btn").html("<i class='fa fa-plus-circle' aria-hidden='true'></i>  Update subscription");
	    		

	    		subscribeSiteSet.empty();
	      		unSubscribeSiteSet.empty();
	      		subscribeKeywordSet.empty();
	      		unsubscribeKeywordSet.empty();
	      		
	      		$(".subscribed-sites").empty();
				$(".nonsubscribed-sites").empty();
				$(".nonsubscribed-keywords").empty();
				$(".subscribed-keywords").empty();
				var subMailVal=allSubscriptions[selectedSubscriptionKey]["email"];
				$("#subscriber-email").val(subMailVal);
				
				var siteListArr=[]
				var keywordListArr=[]
				var keywordsAddedToList=new Set();
				
				var siteId;
				for(siteId in allSubscriptions[selectedSubscriptionKey]["subs"]){
					siteListArr.push(siteId);
					currentSubscribedSites.add("site-"+siteId);
					
					
					$(".subscribed-sites").append("<li id=site-"+siteId+">"+sitesMap.search("site-"+siteId)+"</li>");
		      		subscribeSiteSet.add("site-"+siteId);
		      		
					var keywordId;
					for(keywordId in allSubscriptions[selectedSubscriptionKey]["subs"][siteId]){
						
						
						var ky=allSubscriptions[selectedSubscriptionKey]["subs"][siteId][keywordId];
						keywordListArr.push(ky);
						subscribeKeywordSet.add("keyword-"+ky);
						if(!(keywordsAddedToList.contains(ky))){
							currentSubscribedKeywords.add("keyword-"+ky);
							$(".subscribed-keywords").append("<li id=keyword-"+ky+">"+keywordsMap.search("keyword-"+ky)+"</li>");
						}
							
						keywordsAddedToList.add(ky);
					}
				}
				
				fetchAllSites(allSites,siteListArr);
				fetchAllKeywords(allKeywords,keywordListArr)
				hideShowKeywordSection();
				
	    		
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




function fetchAllKeywords(keywordsList,toOmit){
	if(keywordsList!=null){
		for(var i in keywordsList){
    		
			var isContinue=false;
    		console.log("length "+toOmit.length);
			for(var x=0;x<toOmit.length;x++){
				if(toOmit[x]==i){
					isContinue=true;
					continue;
				}		
			}
			if(isContinue){
				continue;
			}
			else {
				currentNonSubscribedKeywords.add("keyword-"+i);
				$(".nonsubscribed-keywords").append("<li id=keyword-"+i+">"+keywordsList[i]+"</li>");
			}		
				
			
    	}
	}else{
		$.ajax({
	        type: 'GET', // define the type of HTTP verb we want to use
	        url: '/getAllKeywords/', // the url where we want to POST
	        dataType: 'json', // what type of data do we expect back from the server
	        encode: true,
	        success: function (data, textStatus, jqXHR) {
	        	for(var i in data){
	        		allKeywords=data;
	        		keywordsMap.add('keyword-'+i,data[i]);
	        		
	        		$(".nonsubscribed-keywords").append("<li id=keyword-"+i+">"+data[i]+"</li>");
	        	}
	        },
	        error: function (data, textStatus, jqXHR) {
	        	
	        	 $(".nonsubscribed-keywords").append("<li>We faced problems while loading available keywords. Kindly reload page</li>");

	        }

	    });
	}
	
	
}

function fetchAllSites(siteList,toOmit){
	if(siteList!=null){
		for(var i in siteList){
    		var isContinue=false;
			for(var x=0;x<toOmit.length;x++){
				if(toOmit[x]==i){
					isContinue=true;
					continue;
				}		
			}
			if(isContinue) continue;
			else {
				$(".nonsubscribed-sites").append("<li id=site-"+i+">"+siteList[i]+"</li>");
				currentNonSubscribedSites.add("site-"+i);
	
			}
			
    	}
	}else{
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/getAllSites/', // the url where we want to POST
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
        	allSites=data;
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
}

function  closeAlert() {
    $("#alerter").css('display', 'block');
    $("#alerter").fadeTo(3000, 500).slideUp(50, function () {
    $("#alerter").slideUp(50);
    });
}
