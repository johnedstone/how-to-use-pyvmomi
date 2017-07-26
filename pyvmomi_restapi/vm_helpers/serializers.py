# -*- coding: utf-8 -*-
from rest_framework import serializers

from .models import (
    ManageCdrom,
)

class ManageCdromSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ManageCdrom
        fields = '__all__'

        # read_only_fields = fields

# vim: ai et ts=4 sts=4 sw=4 nu ru
