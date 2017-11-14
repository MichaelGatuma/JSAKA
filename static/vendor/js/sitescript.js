var selectedKey=''

$(document).ready(function(){
	
	addBtnEvents();
   
	//url: 'updateContentById?contentId=' + contentId, 
	
	$("button.edit-name").click(function (event) {
		$("div#edit-modal").modal('hide');
		var newname=$("input.edit-name").val();
		editUrl='/edit-name/'+newname+'/'+selectedKey+'/';
		$.ajax({
            type: 'PUT', // define the type of HTTP verb we want to use
            url: editUrl, // the url where we want to POST 
            encode: true,
            success: function (data, textStatus, jqXHR) {
                $("div.alert").removeClass("alert-danger");
                $("div.alert").addClass("alert-success");
                $("p.messageFeedback").text("Edit successful");
                closeAlert();
                fetchAllnames();
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
	
	
	
	
});


function addBtnEvents(){
	 $("button.name").click(function (event) {
	    	selectedKey=event.target.id;
	    	var nameEl='td#'+selectedKey+'-name';
	    	$('input.edit-name').val($(nameEl).html());
	    
	    });
	
}

function fetchAllnames(){

	
	$.ajax({
        type: 'GET', // define the type of HTTP verb we want to use
        url: '/getAllSites/', // the url where we want to POST
        dataType: 'json', // what type of data do we expect back from the server
        encode: true,
        success: function (data, textStatus, jqXHR) {
            $('table#contentItems').find("tr:gt(0)").remove();
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
  	  var trHTML;
  	trHTML +='<tr> <td>' + i + '</td> <td id=\''+i+'-name\'>' + data[i] + '</td>'
  	+	'<td><button type="button" id=\''+i+'\' class="btn btn-info name" data-toggle="modal" style="margin-right:4px;" data-target=".edit-modal">'
	+	'<i class="fa fa-pencil" aria-hidden="true"></i>'
	+'</button>'
	+'</td></tr>'
  	  
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