var global_cur_layer_object
var global_layer_count = 0
// <tr id="image_height">
//   <td>image height:</td>
//   <td>
//       <form id="upload_search_form" target="submitFrame" enctype="multipart/form-data" action="/upload_file" method="post"> 
//           {% csrf_token %} 
//           <input type="text"/>
//       </form>
//   </td>
// </tr>

function create_form(name) {
	table = document.getElementById("leftSideTable");
	tr = document.createElement("tr")
	table.appendChild(tr)
	td = document.createElement("td")
	td.innerHTML = name + ":"
	tr.appendChild(td)
	td = document.createElement("td")
	tr.appendChild(td)
    var form = document.createElement("form");
    form.action = ""
    form.enctype = "multipart/form-data"
    form.method = "post"

    td.appendChild(form)

    input = document.createElement("input")
    input.type = "text"
    input.id = name

    form.appendChild(input)
}

function create_form_with_value(name,param) {
	table = document.getElementById("leftSideTable");
	tr = document.createElement("tr")
	table.appendChild(tr)
	td = document.createElement("td")
	td.innerHTML = name + ":"
	tr.appendChild(td)
	td = document.createElement("td")
	tr.appendChild(td)
    var form = document.createElement("form");
    form.action = ""
    form.enctype = "multipart/form-data"
    form.method = "post"

    td.appendChild(form)

    input = document.createElement("input")
    input.type = "text"
    input.id = name
    input.value = param

    form.appendChild(input)
}



function changeLeftBar() {
	var obj = document.getElementById("LayerSelector"); 
	var index = obj.selectedIndex; 
	var value = obj.options[index].text; 

	var table_node = document.getElementById("leftSideTable")
	var select_node = document.getElementById("select_node").cloneNode(true)
	select_node.getElementsByTagName("select")[0].selectedIndex = index
    while(table_node.childNodes.length>0) {
        table_node.removeChild(table_node.childNodes[0])
    }
    table_node.appendChild(select_node)

	if(value=="DataLayer") {
		create_form("image height")
		create_form("image width")
		create_form("image channel")
	} else if(value=="ConvolutionLayer") {
		create_form("output channel")
		create_form("kernel size")
		create_form("padding")
		create_form("stride")
	} else if(value=="FCLayer") {
		create_form("output channel")
	} else if(value=="PoolingLayer") {
		create_form("kernel size")
		create_form("pooling type")
		create_form("padding")
		create_form("stride")
	}
}


// <tr>
//   <div class="col-md-8 col-sm-8">
//         <button  class="wow fadeInUp btn btn-default section-btn" data-wow-delay="1s" style="background-color:#B00000;">Begin</button>
//   </div>
// </tr>

function create_DataLayer(image_height,image_width,image_channel) {
	var table_node  = document.getElementById("NetworkDisplayer")
	original_node = document.getElementById("newLayerHolder")
	node = original_node.cloneNode(true)
	original_node.id = ""
	button_node = original_node.getElementsByTagName("button")
	console.log(button_node[0].innerHTML)
	button_node[0].innerHTML = "DataLayer"+"/"+image_height+"X"+image_width+"X"+image_channel
	button_node[0].onclick = function() {
		modifyExistingLayer(this);
	};
	button_node[0].id = "MiddleLayer" + global_layer_count.toString()
	global_layer_count++
	var tr_node = document.createElement("tr")
	var td_node =document.createElement("td")
	td_node.appendChild(node)
	tr_node.appendChild(td_node)
	table_node.appendChild(tr_node)
}

function create_ConvolutionLayer(output_channel,kernel_size,padding,stride) {
	var table_node  = document.getElementById("NetworkDisplayer")
	original_node = document.getElementById("newLayerHolder")
	node = original_node.cloneNode(true)
	original_node.id = ""
	button_node = original_node.getElementsByTagName("button")
	console.log(button_node[0].innerHTML)
	button_node[0].innerHTML = "ConvolutionLayer"+"/o"+output_channel+"/k"+kernel_size+"/p"+padding+"/s"+stride
	button_node[0].onclick = function() {
		modifyExistingLayer(this);
	};
	button_node[0].id = "MiddleLayer" + global_layer_count.toString()
	global_layer_count++
	var tr_node = document.createElement("tr")
	var td_node =document.createElement("td")
	td_node.appendChild(node)
	tr_node.appendChild(td_node)
	table_node.appendChild(tr_node)
}


function create_FCLayer(output_channel) {
	var table_node  = document.getElementById("NetworkDisplayer")
	original_node = document.getElementById("newLayerHolder")
	node = original_node.cloneNode(true)
	original_node.id = ""
	button_node = original_node.getElementsByTagName("button")
	console.log(button_node[0].innerHTML)
	button_node[0].innerHTML = "FCLayer"+"/o"+output_channel
	button_node[0].onclick = function() {
		modifyExistingLayer(this);
	};
	button_node[0].id = "MiddleLayer" + global_layer_count.toString()
	global_layer_count++
	var tr_node = document.createElement("tr")
	var td_node =document.createElement("td")
	td_node.appendChild(node)
	tr_node.appendChild(td_node)
	table_node.appendChild(tr_node)
}

function create_PoolingLayer(pooling_type,kernel_size,stride,padding) {
	var table_node  = document.getElementById("NetworkDisplayer")
	original_node = document.getElementById("newLayerHolder")
	node = original_node.cloneNode(true)
	original_node.id = ""
	button_node = original_node.getElementsByTagName("button")
	console.log(button_node[0].innerHTML)
	button_node[0].innerHTML = "PoolingLayer"+"/"+pooling_type+"/k"+kernel_size+"/s"+stride+"/"+padding
	button_node[0].onclick = function() {
		modifyExistingLayer(this);
	};
	button_node[0].id = "MiddleLayer" + global_layer_count.toString()
	global_layer_count++
	var tr_node = document.createElement("tr")
	var td_node =document.createElement("td")
	td_node.appendChild(node)
	tr_node.appendChild(td_node)
	table_node.appendChild(tr_node)
}

function create_BatchNormLayer() {
	var table_node  = document.getElementById("NetworkDisplayer")
	original_node = document.getElementById("newLayerHolder")
	node = original_node.cloneNode(true)
	original_node.id = ""
	button_node = original_node.getElementsByTagName("button")
	console.log(button_node[0].innerHTML)
	button_node[0].innerHTML = "BatchNormLayer"
	button_node[0].onclick = function() {
		modifyExistingLayer(this);
	};
	button_node[0].id = "MiddleLayer" + global_layer_count.toString()
	global_layer_count++
	var tr_node = document.createElement("tr")
	var td_node =document.createElement("td")
	td_node.appendChild(node)
	tr_node.appendChild(td_node)
	table_node.appendChild(tr_node)
}

function create_ReluLayer() {
	var table_node  = document.getElementById("NetworkDisplayer")
	original_node = document.getElementById("newLayerHolder")
	node = original_node.cloneNode(true)
	original_node.id = ""
	button_node = original_node.getElementsByTagName("button")
	console.log(button_node[0].innerHTML)
	button_node[0].innerHTML = "ReluLayer"	
	button_node[0].onclick = function() {
		modifyExistingLayer(this);
	};
	button_node[0].id = "MiddleLayer" + global_layer_count.toString()
	global_layer_count++
	var tr_node = document.createElement("tr")
	var td_node =document.createElement("td")
	td_node.appendChild(node)
	tr_node.appendChild(td_node)
	table_node.appendChild(tr_node)
}

// <tr id="newLayerHolder">
//   <div class="col-md-8 col-sm-8">
//         <button  onclick="createNewLayer()" class="wow fadeInUp btn btn-default section-btn" data-wow-delay="1s" style="background-color:#B00000;"></button>
//   </div>
// </tr>

function CreateLayer() {
	var select_node = document.getElementById("LayerSelector")
	var index = select_node.selectedIndex; 
	var value = select_node.options[index].text; 

	if(value=="DataLayer") {
		image_height = document.getElementById("image height").value; 
		image_width = document.getElementById("image width").value; 
		image_channel = document.getElementById("image channel").value; 		
		create_DataLayer(image_height,image_width,image_channel)
	} else if(value=="ConvolutionLayer") {
		output_channel = document.getElementById("output channel").value; 
		kernel_size = document.getElementById("kernel size").value; 
		padding = document.getElementById("padding").value; 
		stride = document.getElementById("stride").value; 
		create_ConvolutionLayer(output_channel,kernel_size,padding,stride)
	} else if(value=="FCLayer") {
		output_channel = document.getElementById("output channel").value; 
		create_FCLayer(output_channel)
	} else if(value=="PoolingLayer") {
		kernel_size = document.getElementById("kernel size").value; 
		pooling_type = document.getElementById("pooling type").value; 
		padding = document.getElementById("padding").value; 
		stride = document.getElementById("stride").value; 
		create_PoolingLayer(pooling_type,kernel_size,stride,padding)
	} else if(value=="BatchNormLayer") {
		create_BatchNormLayer()
	} else if(value=="ReluLayer") {
		create_ReluLayer()
	}
}

function createNewLayer() {
	var leftSideBarButton = document.getElementById("leftSideBarButton")
	leftSideBarButton.onclick=function() {
		CreateLayer();
	};
	leftSideBarButton.innerHTML="AddLayer"
}

// <tr>
//   <div class="col-md-8 col-sm-8">
//         <button  class="wow fadeInUp btn btn-default section-btn" data-wow-delay="1s" style="background-color:#B00000;">Begin</button>
//   </div>
// </tr>


function modify_DataLayer(image_height,image_width,image_channel) {
	button = global_cur_layer_object
	button.innerHTML = "DataLayer"+"/"+image_height+"X"+image_width+"X"+image_channel
}

function modify_ConvolutionLayer(output_channel,kernel_size,padding,stride) {
	button = global_cur_layer_object
	button.innerHTML = "ConvolutionLayer"+"/o"+output_channel+"/k"+kernel_size+"/p"+padding+"/s"+stride
}

function modify_FCLayer(output_channel) {
	button = global_cur_layer_object
	button.innerHTML = "FCLayer"+"/o"+output_channel
}

function modify_PoolingLayer(pooling_type,kernel_size,stride,padding) {
	button = global_cur_layer_object
	button.innerHTML = "PoolingLayer"+"/"+pooling_type+"/k"+kernel_size+"/s"+stride+"/"+padding
}

function modify_BatchNormLayer() {
	button = global_cur_layer_object
	button.innerHTML = "BatchNormLayer"	
}

function modify_ReluLayer() {
	button = global_cur_layer_object
	button.innerHTML = "ReluLayer"	
}

function modifyLayer() {
	var select_node = document.getElementById("LayerSelector")
	var index = select_node.selectedIndex; 
	var value = select_node.options[index].text; 

	if(value=="DataLayer") {
		image_height = document.getElementById("image height").value; 
		image_width = document.getElementById("image width").value; 
		image_channel = document.getElementById("image channel").value; 
		modify_DataLayer(image_height,image_width,image_channel)
	} else if(value=="ConvolutionLayer") {
		output_channel = document.getElementById("output channel").value; 
		kernel_size = document.getElementById("kernel size").value; 
		padding = document.getElementById("padding").value; 
		stride = document.getElementById("stride").value; 
		modify_ConvolutionLayer(output_channel,kernel_size,padding,stride)
	} else if(value=="FCLayer") {
		output_channel = document.getElementById("output channel").value; 
		modify_FCLayer(output_channel)
	} else if(value=="PoolingLayer") {
		pooling_type = document.getElementById("pooling type").value; 
		kernel_size = document.getElementById("kernel size").value; 
		padding = document.getElementById("padding").value; 
		stride = document.getElementById("stride").value; 
		modify_PoolingLayer(pooling_type,kernel_size,stride,padding)
	} else if(value=="BatchNormLayer") {
		modify_BatchNormLayer()
	} else if(value=="ReluLayer") {
		modify_ReluLayer()
	}

}

function Parse_DataLayer() {
	var layer = global_cur_layer_object
	var content = layer.innerHTML
	content = content.split("/")
	content = content[1].split("X")
	return content	
}

function Parse_ConvolutionLayer() {
	var layer = global_cur_layer_object
	var content = layer.innerHTML
	console.log(content)
	content = content.split("/o")
	console.log(content)
	content = content[1].split("/k")
	console.log(content)
	output_channel = content[0]
	content = content[1].split("/p")
	console.log(content)
	kernel_size = content[0]
	content = content[1].split("/s")
	console.log(content)
	padding = content[0]
	stride = content[1]
	return [output_channel,kernel_size,padding,stride]
}

function Parse_FCLayer() {
	var layer = global_cur_layer_object
	var content = layer.innerHTML
	content = content.split("/o")
	output_channel = content[1]
	return output_channel
}

function Parse_PoolingLayer() {
	var layer = global_cur_layer_object
	var content = layer.innerHTML
	content = content.split("/")
	pooling_type = content[1]
	kernel_size = content[2].slice(1)
	stride = content[3].slice(1)
	padding = content[4]
	return [kernel_size,pooling_type,padding,stride]
}


function modifyExistingLayer(element) {
	var leftSideBarButton = document.getElementById("leftSideBarButton")
	leftSideBarButton.onclick=function(){
		modifyLayer();
	};
	leftSideBarButton.innerHTML="ModifyLayer"
	global_cur_layer_object = element

	var value = (element.innerHTML.split("/"))[0]

	var obj = document.getElementById("LayerSelector"); 
	var index = 0
	for(;index<obj.options.length;index++) {
		if(obj.options[index].text==value)
			break;
	}

	var table_node = document.getElementById("leftSideTable")
	var select_node = document.getElementById("select_node").cloneNode(true)
	select_node.getElementsByTagName("select")[0].selectedIndex = index
    while(table_node.childNodes.length>0) {
        table_node.removeChild(table_node.childNodes[0])
    }
    table_node.appendChild(select_node)

	if(value=="DataLayer") {
		var param = Parse_DataLayer()
		create_form_with_value("image height",param[0])
		create_form_with_value("image width",param[1])
		create_form_with_value("image channel",param[2])
		console.log(param)
	} else if(value=="ConvolutionLayer") {
		var param = Parse_ConvolutionLayer()
		create_form_with_value("output channel",param[0])
		create_form_with_value("kernel size",param[1])
		create_form_with_value("padding",param[2])
		create_form_with_value("stride",param[3])
	} else if(value=="FCLayer") {
		var param = Parse_FCLayer()
		create_form_with_value("output channel",param)
	} else if(value=="PoolingLayer") {
		var param = Parse_PoolingLayer()
		create_form_with_value("kernel size",param[0])
		create_form_with_value("pooling type",param[1])
		create_form_with_value("padding",param[2])
		create_form_with_value("stride",param[3])
	}
}


function submitNetwork() {
	var json = {}
	json.layer = []
	for(var i=0;i<global_layer_count;i++) {
		var layer_id = "MiddleLayer" + i.toString()
		layer_obj = document.getElementById(layer_id)
		global_cur_layer_object = layer_obj
		// console.log(layer_obj.innerHTML)
		var value = (layer_obj.innerHTML.split("/"))[0]
		if(value=="DataLayer") {
			var param = Parse_DataLayer()
			data_layer = {}
			data_layer.layer_type = "DataLayer"
			data_layer.image_height = param[0]
			data_layer.image_width = param[1]
			data_layer.image_channel = param[2]
			json.layer.push(data_layer)
		} else if(value=="ConvolutionLayer") {
			var param = Parse_ConvolutionLayer()
			conv_layer = {}
			conv_layer.layer_type = "ConvolutionLayer"
			conv_layer.output_channel = param[0]
			conv_layer.kernel_size = param[1]
			conv_layer.padding = param[2]
			conv_layer.stride = param[3]
			json.layer.push(conv_layer)
		} else if(value=="FCLayer") {
			var param = Parse_FCLayer()
			fc_layer = {}
			fc_layer.layer_type = "FCLayer"
			fc_layer.output_channel = param
			json.layer.push(fc_layer)
		} else if(value=="PoolingLayer") {
			var param = Parse_PoolingLayer()
			pooling_layer = {}
			pooling_layer.layer_type = "PoolingLayer"
			pooling_layer.kernel_size = param[0]
			pooling_layer.pooling_type = param[1]
			pooling_type.padding = param[2]
			pooling_type.stride = param[3]
			json.layer.push(pooling_layer)
		} else if(value=="ReluLayer") {
			relu_layer = {}
			relu_layer.layer_type = "ReluLayer"
			json.layer.push(relu_layer)
		} else if(value=="BatchNormLayer") {
			batch_norm_layer = {}
			batch_norm_layer.layer_type = "BatchNormLayer"
			json.layer.push(batch_norm_layer)
		}
	}

	var jsonStr = JSON.stringify(json);
	console.log(jsonStr)
}