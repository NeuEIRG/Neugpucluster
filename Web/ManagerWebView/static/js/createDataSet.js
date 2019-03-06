

$(function(){
    $("#upload_search_form").ajaxForm(function(message) { 
        console.log(message['dataset_name'])
        console.log(message['class_name'])
        if(message['status']=="success") {
            alert("upload over!")

            var table_node = document.getElementById('ImageDisplayer');
            while(table_node.childNodes.length>0) {
                table_node.removeChild(table_node.childNodes[0])
            }

            var text_node = document.getElementById('TopRightText');
            text_node.innerHTML = message['dataset_name']

            for(var key in message['class_name']) {
                tr = document.createElement("tr");
                td = document.createElement("td");
                table_node.appendChild(tr)
                tr.appendChild(td)
                td.innerHTML = key
                for(var i=0,len=message['class_name'][key].length;i<len;i++) {
                    img_name = message['class_name'][key][i]
                    td = document.createElement("td");
                    tr.appendChild(td)
                    img = document.createElement("img")
                    td.appendChild(img)
                    img.src = '/static/images/' + message['dataset_name'] + '/' + key + '/' + img_name
                }
            }

        } else {
            alert("upload failed!")
        }
    });   
});
