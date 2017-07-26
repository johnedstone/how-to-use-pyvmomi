# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import (
    viewsets,
)

from .models import (
    ManageCdrom,
)

from .serializers import (
    ManageCdromSerializer,
)

class ManageCdromViewSet(viewsets.ModelViewSet):
    queryset = ManageCdrom.objects.all()
    serializer_class = ManageCdromSerializer
    #http_method_names = ['get']
