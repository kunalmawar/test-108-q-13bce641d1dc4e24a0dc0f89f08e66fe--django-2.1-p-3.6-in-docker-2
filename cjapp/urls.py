"""cjapp URL Configuration

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
from restapi.views import *


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^create', UserAPIView.as_view(), name='create-user'),
    url(r'^add/(?P<userA>[\w\-]+)/(?P<userB>[\w\-]+)', SendFriendRequest.as_view(), name='friend-request'),
    url(r'^friendRequests/(?P<userA>[\w\-]+)', GetPendingRequests.as_view(), name='pending-requests'),
    url(r'^friends/(?P<userA>[\w\-]+)', GetAllFriends.as_view(), name='get-all-friends'),
    url(r'^suggestions/(?P<userA>[\w\-]+)', GetAllFriendSuggestions.as_view(), name='get-all-friend-suggestions'),
]
