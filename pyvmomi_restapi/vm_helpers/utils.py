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
    vmname_data = request.data.get('vmname', None)
    vsphere_service_data = request.data.get('vsphere_service', None)

    logger.info('state_data: {}'.format(state_data))

    if not state_data:
        detail['state'] = ["""This field is required: {} """.format(CHOICES)]

    if not vmname_data:
        detail['vmname'] = ["""This field is required"""]

    if not vsphere_service_data:
        detail['vsphere_service'] = ["""This field is required"""]

    if state_data and state_data not in STATE_CHOICES:
        detail['state'] = ["""{} is not a valid choice: {} """.format(state_data, CHOICES)]

    if state_data and state_data == 'mount' and not iso_path_data:
        detail['iso_path'] = ["""This field is required when state = mount"""]

    if state_data and state_data == 'umount' and iso_path_data:
        detail['iso_path'] = ["""This field is not required when state = umount"""]

    return detail

# vim: ai et ts=4 sw=4 sts=4 nu ru
