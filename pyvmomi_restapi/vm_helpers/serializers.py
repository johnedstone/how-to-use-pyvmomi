# -*- coding: utf-8 -*-
import logging

from django.conf import settings
from rest_framework import serializers

from .models import (
    ManageCdrom,
)

logger = logging.getLogger(settings.PROJECT_LOGGING)

class ManageCdromSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ManageCdrom
        fields = '__all__'

        # read_only_fields = fields

# vim: ai et ts=4 sts=4 sw=4 nu ru
