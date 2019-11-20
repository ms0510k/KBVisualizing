"""DjangoTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from polls import views

app_name = "polls"

urlpatterns = [
    url(r'^$', views.ontologyDemo, name="ontologyDemo"),
    url(r'^ontologyDemo/graph/$', views.graph, name='graph'),
    url(r'^ontologyDemo/stt/$', views.stt, name='stt'),
    url(r'^ontologyDemo/depth/$', views.depth, name='depth'),
    url(r'^ontologyDemo/targetProperty/$', views.targetProperty, name='targetProperty'),
    url(r'^ontologyDemo/delTriple/$', views.delTriple, name='delTriple'),
    url(r'^ontologyDemo/runEngine/$', views.runEngine, name='runEngine'),
    url(r'^ontologyDemo/objectReasoning/$', views.objectReasoning, name='objectReasoning'),
    url(r'^ontologyDemo/relationReasoning/$', views.relationReasoning, name='relationReasoning'),
    url(r'^ontologyDemo/inferredOnly/$', views.inferredOnly, name='inferredOnly'),
    url(r'^ontologyDemo/Reasoning/$', views.Reasoning, name='Reasoning'),
]