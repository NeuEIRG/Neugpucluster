

$(function(){
    $("#upload_search_form").ajaxForm(function(message) { 
        var div_node = document.getElementById('resultDisplay');
        while(div_node.childNodes.length>0) {
            div_node.removeChild(div_node.childNodes[0])
        }  
        var p_node = document.createElement("h1");
        p_node.style = "position:absolute;left:700px;top:300px;"
        p_node.innerHTML = message["args"]
        div_node.appendChild(p_node) 

        var upload_node = document.getElementById('uploadDisplay');
        while(upload_node.childNodes.length>0) {
            upload_node.removeChild(upload_node.childNodes[0])
        }       
        upload_img = document.createElement("img");
        upload_img.src="/static/images/temp/"+message['file_src']
        console.log(message['file_src'])
        style_str="position:absolute;height:300px;width:300px;left:10px;top:180px;"
        upload_img.style=style_str
        upload_node.appendChild(upload_img) 
    });   
});

