# -*- coding: utf-8 -*-
import logging, os, shlex, subprocess
import jsonpickle
from threading import Timer

from django.conf import settings

logger = logging.getLogger(settings.PROJECT_LOGGING)

def manage_cdrom(obj):
    """ https://www.blog.pythonlibrary.org/2016/05/17/python-101-how-to-timeout-a-subprocess/

    Waiting for: Python 3.5 added the run function which accepts a timeout parameter. 
    """
  
    kill = lambda process: process.kill()

    class Result(object):

       def __init__(self):
           self.ok = False
           self.stdout = ''
           self.stderr = ''
           self.returncode = 99 
        

    result = Result()
    user = settings.VSPHERE_USERNAME
    passwd = settings.VSPHERE_PASSWORD
    vsphere_service = ''
    vmname = ''
    iso = ''

    cwd = os.path.dirname(__file__)
    logger.debug('path: {}'.format(cwd))
    if obj.state == 'mount':
        cmd = """python {cwd}/change_vm_cd_backend_with_answer.py -u '{user}' -p '{passwd}' -s '{vsphere_service}' -n '{vmname}' -m {unit_number} -i '{iso}'""".format(
                  cwd=cwd,
                  user=user,
                  passwd=passwd,
                  vsphere_service=obj.vsphere_service,
                  vmname=obj.vmname,
                  unit_number=obj.unit_number,
                  iso=obj.iso_path,
              )
    elif obj.state == 'umount':
        cmd = """python {cwd}/change_vm_cd_backend_with_answer.py -u '{user}' -p '{passwd}' -s '{vsphere_service}' -n '{vmname}' -m {unit_number}""".format(
                  cwd=cwd,
                  user=user,
                  passwd=passwd,
                  vsphere_service=obj.vsphere_service,
                  unit_number=obj.unit_number,
                  vmname=obj.vmname,
              )
    else:
        result.stderr = 'Command is mangled: check with the application ownder'
        result.returncode = 98
        return result

    logger.debug('Command: {}'.format(cmd))
    p1 = subprocess.Popen(shlex.split(cmd),
             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
             env={'a': 'b'})
             # env={'ITERATIONS_WAITING_FOR_BLOCKING_QUESTION': settings.ITERATIONS_WAITING_FOR_BLOCKING_QUESTION})
    my_timer = Timer(settings.PVMOMI_TIMEOUT, kill, [p1])

    try:
        my_timer.start()
        result.stdout, result.stderr = p1.communicate()
        result.returncode =  p1.returncode
    finally:
        my_timer.cancel()

    if result.returncode == 0:
        result.ok = True

    if result.returncode == -9:
        result.stderr += 'Call to cdrom killed by the Timer'

    logger.debug(jsonpickle.encode(result))
    return result

# vim: ai et ts=4 sw=4 sts=4 nu ru
