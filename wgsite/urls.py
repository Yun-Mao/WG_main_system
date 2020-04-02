from django.conf.urls import url
from django.urls import path,include
from . import views
app_name = 'wgsite'
urlpatterns = [
    # ex: /wgsite/
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name='register'),
    path('findpassword', views.findPassword, name='findpassword'),
    path('wsxx', views.wsxx, name='wsxx'),
    path('mp', views.mp, name='mp'),
    path('bsproject', views.bsproject, name='bsproject'),
    url(r'^ebsproject/(?P<id>\d+)/$', views.ebsproject, name="ebsproject"),
    path('bmbsproject', views.bmbsproject, name='bmbsproject'),
    path('abmbsproject', views.abmbsproject, name='abmbsproject'),
    path('lbmbsproject', views.lbmbsproject, name='lbmbsproject'),
    path('showbm', views.showbm, name='showbm'),
    path('dcbsproject', views.dcbsproject, name='dcbsproject'),
    path('weibo', views.weibo, name='weibo'),
    path('nofound', views.nofound, name='404'),
]