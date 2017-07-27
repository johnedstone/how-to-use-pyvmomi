# -*- coding: utf-8 -*-
import logging, shlex, subprocess
import jsonpickle
from threading import Timer

from django.conf import settings

logger = logging.getLogger(settings.PROJECT_LOGGING)

def manage_cdrom(obj):
    """ https://www.blog.pythonlibrary.org/2016/05/17/python-101-how-to-timeout-a-subprocess/

    Waiting for: Python 3.5 added the run function which accepts a timeout parameter. 
    """
  
    kill = lambda process: process.kill()
    cmd = 'echo boo'

    class Result(object):

       def __init__(self):
           self.ok = False
           self.stdout = ''
           self.stderr = ''
           self.returncode = 99 
        

    result = Result()

    p1 = subprocess.Popen(shlex.split(cmd),
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    my_timer = Timer(30, kill, [p1])

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

    logger.info(jsonpickle.encode(result))
    return result

# vim: ai et ts=4 sw=4 sts=4 nu ru
