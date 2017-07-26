from django.conf.urls import url, include  
from django.shortcuts import redirect

from vm_helpers.urls import router as vm_helpers_router

urlpatterns = [  
    url(r'^$', lambda x: redirect('/api/', permanent=False), name='home'),
    url(r'^api/', include(vm_helpers_router.urls)),
]
