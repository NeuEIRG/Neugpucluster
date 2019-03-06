

$(function(){
    $("#upload_search_form").ajaxForm(function(message) { 
        if(message=="over") {
            alert("Start Training!")
        } else {
            alert("Request Failed!")
        }
    });   
});
