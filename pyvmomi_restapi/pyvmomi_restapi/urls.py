from django.conf.urls import url, include  
from django.shortcuts import redirect

from rest_framework_swagger.views import get_swagger_view

from vm_helpers.urls import router as vm_helpers_router

schema_view = get_swagger_view(title='IIHS INFRASTRUCTURE REST API')

urlpatterns = [  
    url(r'^$', lambda x: redirect('/api/', permanent=False), name='home'),
    url(r'^swagger/$', schema_view),
    url(r'^api/', include(vm_helpers_router.urls)),
    url(r'^liveness/', lambda request:HttpResponse(status=200)),
    url(r'^readiness/', lambda request:HttpResponse(status=200)),
]
