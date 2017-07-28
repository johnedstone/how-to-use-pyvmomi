# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.conf import settings

from rest_framework import (
    viewsets,
)

from rest_framework.exceptions import (ParseError, NotFound)

from .models import (
    ManageCdrom,
)

from .utils import (
    check_state,
)

from .serializers import (
    ManageCdromSerializer
)

logger = logging.getLogger(settings.PROJECT_LOGGING)

class ManageCdromViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return a given cdrom transaction

    list:
    Return a list of cdrom transactions

    create:
    Mount or umount a cdrom for a VM
    """

    queryset = ManageCdrom.objects.all()
    serializer_class = ManageCdromSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        detail = check_state(request)
        logger.info('detail: {}'.format(detail))
        if detail:
            raise ParseError(detail=detail)

        response = super(ManageCdromViewSet, self).create(request, *args, **kwargs)

        return response


# vim: ai et ts=4 sw=4 sts=4 nu ru
