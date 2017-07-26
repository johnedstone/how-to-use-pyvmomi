from django.conf.urls import url, include  
from django.shortcuts import redirect

from helper_endpoints.urls import router as helper_endpoints_router

urlpatterns = [  
    url(r'^$', lambda x: redirect('/api/', permanent=False), name='home'),
    url(r'^api/', include(helper_endpoints_router.urls)),
]
