# -*- coding: utf-8 -*-
import logging

from django.conf import settings

logger = logging.getLogger(settings.PROJECT_LOGGING)
STATE_CHOICES = [choice[0] for choice in settings.STATE_CHOICES]
CHOICES = " or ".join(STATE_CHOICES)

def check_state(request):

    detail = {}

    state_data = request.data.get('state', None)
    iso_path_data = request.data.get('iso_path', None)

    logger.info('state_data: {}'.format(state_data))

    if not state_data:
        detail['state'] = ["""This paramater is required: {} """.format(CHOICES)]

    if state_data and state_data not in STATE_CHOICES:
        detail['state'] = ["""This paramater is required: {} """.format(CHOICES)]

    if state_data and state_data == 'mount' and not iso_path_data:
        detail['iso_path'] = ["""This paramater is required when state = mount"""]

    return detail

# vim: ai et ts=4 sw=4 sts=4 nu ru
