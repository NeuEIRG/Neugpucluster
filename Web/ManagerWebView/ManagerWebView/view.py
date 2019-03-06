from django.http import HttpResponse
from django.shortcuts import render
import json
import os
import sys
from django.views.decorators.csrf import csrf_exempt
import simplejson
  

def hello(request):
    return render(request,'index.html')

def page_1(request):
    return render(request,'page_1.html')

def page_2(request):
    return render(request,'page_2.html')

def page_3(request):
    return render(request,'page_3.html')

def showExistingDataSets(request):
	return render(request,'showExistingDataSets.html')

def createDataSet(request):
	return render(request,'createDataSet.html')

def createNetwork(request):
	return render(request,'createNetwork.html')

def train(request):
	return render(request,'train.html')

def test(request):
	return render(request,"test.html")

def upload_file(request):
	if request.POST:
		images =request.FILES.getlist("upload_images")
		dataset_name = request.POST['dataset_name']
		class_name = request.POST['class_name'] 
		# print(len(images))
		base_dir = os.path.abspath('./static/images/') + '/'
		if not os.path.exists(base_dir+dataset_name):
		    os.mkdir(base_dir+dataset_name)
		if not os.path.exists(base_dir+dataset_name+'/'+class_name):
			os.mkdir(base_dir+dataset_name+'/'+class_name)
		for img in images:
			# print(f.name)
			destination = open(base_dir+dataset_name+'/'+class_name+'/'+img.name,'wb')   
			for chunk in img.chunks():      
			    destination.write(chunk)  
			destination.close()  

		class_dict = {}
		classes = os.listdir(base_dir+dataset_name)
		for cs in classes:
			imgs = os.listdir(base_dir+dataset_name+"/"+cs)
			if len(imgs)>5:
				imgs = imgs[:5]
			class_dict[cs] = imgs

		json_results = {}
		json_results['status'] = "success"
		json_results['class_name'] = class_dict
		json_results['dataset_name'] = dataset_name
		return HttpResponse(json.dumps(json_results), content_type='application/json')

@csrf_exempt
def upload_network(request):
	if request.POST:
		json_data = simplejson.loads(request.body)
		print(json_data)
		return HttpResponse("over")
	else:
		return HttpResponse("fail")


def upload_train_options(request):
	if request.POST:
		
		return HttpResponse("over")
	else:
		return HttpResponse("fail")
