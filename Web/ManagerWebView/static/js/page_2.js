

$(function(){
    $("#upload_search_form").ajaxForm(function(message) { 
        var upload_node = document.getElementById('uploadDisplay');
        while(upload_node.childNodes.length>0) {
            upload_node.removeChild(upload_node.childNodes[0])
        }       

        var upload_img = document.createElement("img")
        upload_img.src="/static/images/temp/"+message['file_src']
        var style_str="position:absolute;height:300px;width:300px;left:10px;top:180px;"
        upload_img.style=style_str
        upload_node.appendChild(upload_img) 
        
        delete message['file_src']

        var div_node = document.getElementById('resultDisplay');
        while(div_node.childNodes.length>0) {
            div_node.removeChild(div_node.childNodes[0])
        }
        var left_pos = 350
        var top_pos = 180
        var count = 0
        for(var key in message){
            var img = document.createElement("img");
            img.src="/static/images/"+message[key]

            style_str="position:absolute;height:100px;width:100px;"+"left:"+left_pos.toString()+"px;top:"+top_pos.toString()+"px;"
            img.style=style_str     
            img.id="img"+count.toString()
        　　$(img).click(function(){
                var current_target=event.target
                var body_node = document.getElementById('bd');
                var src = current_target.src 
                var div_node = document.createElement("div");   
                var div_img_node = document.createElement("img");
                div_node.style="position:absolute;width:100%;height:100%;background-color:rgba(200,200,200,0.8);z-index:9999"
                div_node.appendChild(div_img_node)
                div_node.id="div_temp"
                div_img_node.src=src 
                div_img_node.style="position:absolute;left:390px;top:83px;height:500px;width:500px"
                body_node.appendChild(div_node)
                $(div_img_node).click(function(){
                    var sub_body_node = document.getElementById('bd');
                    var sub_div_node = document.getElementById('div_temp');
                    while(sub_div_node.childNodes.length>0) {
                        sub_div_node.removeChild(sub_div_node.childNodes[0])
                    }

                    sub_body_node.removeChild(sub_div_node)
                })
            })
            div_node.appendChild(img)  

            left_pos=left_pos+150
            count = count +1 
            if(count%4==0) {
                left_pos = 350
                top_pos = top_pos + 150
            }

         }
    });   
});