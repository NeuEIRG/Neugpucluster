

$(function(){
    $("#upload_search_form").ajaxForm(function(message) { 
        alert("upload success")
    });   
});



function load_function() {
    // var ul = document.getElementById('table');
    // var li = document.createElement("li");
    // var a = document.createElement("a");
    // ul.appendChild(li);
    // li.appendChild(a);
    // a.innerHTML = "数据（可以去循环出想要的数据）";　

    // xmlhttp =new XMLHttpRequest();
    // xmlhttp.open("GET","/img_num",true);
    // xmlhttp.send();
    // console.log(JSON.stringify(xmlhttp.responseText));

    var table_node = document.getElementById('table');
    while(table_node.childNodes.length>0) {
        table_node.removeChild(table_node.childNodes[0])
    }


    $.getJSON('/img_class',function(ret){
    　　for(var key in ret){   
            tb = document.createElement("li");
            table_node.appendChild(tb)
            ta = document.createElement("a");
            tb.appendChild(ta)
            ta.id=ret[key]
            ta.innerHTML=ret[key]
        }
    })


    $('#tab ul').on('click','li',function(){
        var img_node = document.getElementById('displayfiles');
        while(img_node.childNodes.length>0) {
            img_node.removeChild(img_node.childNodes[0])
        }

        var current_id=event.target.id

        $.ajax({
            url:"/img_num", 
            type:"POST", 
            data:{"args":current_id,"csrfmiddlewaretoken":$("[name='csrfmiddlewaretoken']").val()}, 
            success:function(ret) { 　　　　　　
                var num=ret['re']    
                var left_pos=150
                var top_pos=200
                var img_count=0
                console.log(num)
                for(var id=1;id<=num;id++) {
                    str="/static/images/"+current_id+"/"+id.toString()+".jpg"
                    console.log(str)
                    img = document.createElement("img");
                    img_node.appendChild(img)
                    img.src=str
                    style_str="position:absolute;"+"left:"+left_pos.toString()+"px;top:"+top_pos.toString()+"px;"
                    img.style=style_str
                    img.height="200" 
                    img.width="200"
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
                    left_pos=left_pos+250
                    img_count++
                    if(img_count%4==0) {
                        top_pos=top_pos+250
                        left_pos=150
                    }
                }
    
            }
        })
        // $.getJSON('/img_num',function(ret){
        // })
    })
}





