from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from . import views,login


urlpatterns = [
    url(r'expertInfo/',views.expertInfo_api),
    url(r'domains',views.domains),
    url(r'project/',views.project_api),
    url(r'projects',views.projects),
    url(r'searchExperts',views.searchExperts),
    url(r'createPool',views.createPool),
    url(r'groupMember',views.groupMember),
    url(r'accountInfo',views.accountInfo)
]


