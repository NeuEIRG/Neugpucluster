"""ManagerWebView URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
 
from . import view

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^$', view.hello),
    url(r'page_1$',view.page_1),
    url(r'page_2$',view.page_2),
    url(r'page_3$',view.page_3),
    url(r'showExistingDataSets$',view.showExistingDataSets),
    url(r'createDataSet$',view.createDataSet),
    url(r'upload_file$',view.upload_file),
    url(r'createNetwork$',view.createNetwork),
    url(r'upload_network$',view.upload_network),
]
