
from django.conf.urls import url , include
from django.contrib import admin
from . import views

urlpatterns = [

    url(r'^$', views.sign_up),  #url(r'^admin/', admin.site.urls),
    url(r'^login/',views.login),
    url(r'^feed/', views.feed),
    url(r'^upload/',views.upload),
    url(r'^like/' ,views.like_view),
    url(r'^comment/',views.make_comment),
    url(r'^logout/',views.logout),
    url(r'^user_info',views.user_info)
,
]
