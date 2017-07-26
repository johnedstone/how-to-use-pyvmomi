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

    vmname = models.CharField(max_length=100)
    vcenter = models.CharField(max_length=100)
    state = models.CharField(choices=STATE_CHOICES, max_length=25)
    iso_path = models.CharField(max_length=200, help_text='[datastore] path/to/iso', blank=True )
    
    stdout = models.TextField(max_length=100, default='', help_text='No need to edit')
    stderr = models.TextField(max_length=100, default='', help_text='No need to edit')
    status_code = models.IntegerField(default=99, help_text='No need to edit')
    status = models.CharField(max_length=20, default='pending', help_text='No need to edit')

    class Meta:
        ordering = ['vmname']

    def __str__(self):
        return self.vmname

    def save(self, *args, **kwargs):
        try:
            logger.info('vmname: {}'.format(self.vmname))
            result = manage_cdrom(self)
            if result and result['ok']:
                pass #self.status_code = result.status_code
#                self.stdout = result.json()
#                self.status = "Finished"
            else:
                pass#self.status_code = 'unknown'
#                self.stdout = 'unknown'
#                self.status = 'unknown'
        except Exception as e:
            self.stderr = '{}'.format(e)
            self.status = 'failed'
            raise(e)
#        finally:
#            pass
#
        super(ManageCdrom, self).save(*args, **kwargs)

# vim: ai et ts=4 sw=4 sts=4 nu ru
