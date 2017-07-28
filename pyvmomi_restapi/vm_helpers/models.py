# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from manage_cdrom import manage_cdrom

logger = logging.getLogger(settings.PROJECT_LOGGING)

class TimeStampModel(models.Model):
    """
    An abstract base class model that provide self-
    updating 'created' and 'modified' fields.
    """
    created =  models.DateTimeField(auto_now_add=True)
    # modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

@python_2_unicode_compatible
class ManageCdrom(TimeStampModel):
    '''Used to log transactions'''

    STATE_CHOICES = settings.STATE_CHOICES

    iso_path = models.CharField(max_length=200, help_text='[datastore] path/to/iso', blank=True )
    unit_number = models.IntegerField(default=1, help_text='CD/DVD unit number. Default=1')

    vmname = models.CharField(max_length=100)
    vsphere_service = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=25)
    
    shell_returncode = models.IntegerField(default=999, help_text='read only')
    status = models.CharField(max_length=20, default='pending', help_text='read only')
    stdout = models.TextField(max_length=100, default='', help_text='read only')
    stderr = models.TextField(max_length=100, default='', help_text='read only')

    class Meta:
        ordering = ['vmname']

    def __str__(self):
        return self.vmname

    def save(self, *args, **kwargs):
        try:
            logger.info('vmname: {}'.format(self.vmname))
            result = manage_cdrom(self)

            self.shell_returncode = result.returncode
            self.stdout = result.stdout
            self.stderr = result.stderr

            if result.ok:
                self.status = "Success"
                if 'VM not found' in self.stdout:
                    self.status = 'Failed'
            else:
                self.status = 'Failed'
        except Exception as e:
            self.stderr = '{}'.format(e)
            self.status = 'Failed: Exception thrown'

        finally:
            return super(ManageCdrom, self).save(*args, **kwargs)

# vim: ai et ts=4 sw=4 sts=4 nu ru
