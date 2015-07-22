from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'WaterSystem.views.home', name='home'),
    # url(r'^WaterSystem/', include('WaterSystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'sensorcontrol.views.index'),
    url(r'^verifycode/$', 'sensorcontrol.views.verifycode'),
    url(r'^main/(?P<user>\w{1,20})', 'sensorcontrol.views.main', name="main"),
    url(r'^logout/', 'sensorcontrol.views.logout'),
    url(r'^storagemanage/$', 'sensorcontrol.views.storagemanage', name="storagemanage"),
    url(r'^storagemonitor/$', 'sensorcontrol.views.storagemonitor'),
    # url(r'^storagemonitor/(?P<user2>\w{8,20})', 'sensorcontrol.views.storagemonitor2', name="storagemonitor"),
    url(r'^delete/(?P<index>\d{1,3})', 'sensorcontrol.views.delete'),
    url(r'^add/$', 'sensorcontrol.views.add'),
    url(r'^test/(?P<storage>\d{1,3})/(?P<type>\w{1,10})/(?P<year>\d{1,4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})-(?P<hour>\d{1,2})-(?P<min>\d{1,2})/$', 'sensorcontrol.views.circlegraph'),
    url(r'^test2/(?P<storage>\d{1,3})/(?P<sensor>\d{1,3})/(?P<year1>\d{1,4})-(?P<month1>\d{1,2})-(?P<day1>\d{1,2})-(?P<hour1>\d{1,2})-(?P<min1>\d{1,2})/(?P<year2>\d{1,4})-(?P<month2>\d{1,2})-(?P<day2>\d{1,2})-(?P<hour2>\d{1,2})-(?P<min2>\d{1,2})/$', 'sensorcontrol.views.linegraph'),
    #url(r'^write/(?P<type>\w{1,20})/(?P<num>\d{1,5})/(?P<sensor>\d{1,3})/(?P<storage>\d{1,3})/$', 'sensorcontrol.views.write'),
    url(r'^storagemonitor/(?P<storage>\d{1,5})/(?P<type>\w{1,20})/$', 'sensorcontrol.views.getsensorlist'),
    url(r'^storagemonitor/(?P<storage>\d{1,5})/$', 'sensorcontrol.views.gettype'),
    url(r'^storagemanage/(?P<storage>\d{1,5})/$', 'sensorcontrol.views.getsensorlist2')

)