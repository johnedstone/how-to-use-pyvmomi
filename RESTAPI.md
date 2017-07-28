## Description

The scripts in the custom_scripts directory in this repository can be
exposed as REST API endpoints.  This project describes an example using
the [Django Rest Framework](http://www.django-rest-framework.org/).  This django
project is written for PaaS, specifically Openshift.  But it can be adapted on
any platform that Django runs on.

## Setup
```
cd pyvmomi_restapi
pip install requirements.txt
python manage.py migrate

# Develop/Debug
export DEBUG=on SPHERE_USERNAME='someusername' VSPHERE_PASSWORD='somepassword'
python manage.py runserver
```

## Swagger
Swagger documentation URL: /swagger/

## Usage
Note: in these examples the python project [HTTPie](https://httpie.org/) is used in place of curl

### What is success?
A `mount` or `umount`, to be successful will return two fields:

* shell_returncode: 0
* status: Success

If these two fields are display with 0 and Success, respectively
examine these fields:

* stderr
* stdout


### Mount and Umount

```
http POST http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/ state=mount vsphere_service=vshpere_service vmname='vmname' iso_path='[datastore] path/some.iso'
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 466
Content-Type: application/json
Date: Fri, 28 Jul 2017 15:45:11 GMT
Location: http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/6/
Server: WSGIServer/0.1 Python/2.7.5
X-Frame-Options: SAMEORIGIN

{
    "created": "2017-07-28T15:45:11.719565Z",
    "iso_path": "[datastore] path/some.iso",
    "shell_returncode": 0,
    "state": "mount",
    "status": "Success",
    "stderr": "",
    "stdout": "Searching for VM vmname\nVM CD/DVD 1 successfully state changed to [datastore] path/some.iso\n",
    "unit_number": 1,
    "url": "http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/6/",
    "vsphere_service": "vshpere_service",
    "vmname": "vmname"
}


http POST http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/ state=umount vsphere_service=vshpere_service vmname='vmname'
HTTP/1.0 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 401
Content-Type: application/json
Date: Fri, 28 Jul 2017 15:45:53 GMT
Location: http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/7/
Server: WSGIServer/0.1 Python/2.7.5
X-Frame-Options: SAMEORIGIN

{
    "created": "2017-07-28T15:45:52.982759Z",
    "iso_path": "",
    "shell_returncode": 0,
    "state": "umount",
    "status": "Success",
    "stderr": "",
    "stdout": "Searching for VM vmname\nThe Question has been answered 'Yes'. The CDRom is disconnected\nVM CD/DVD 1 successfully state changed to Client Device\n",
    "unit_number": 1,
    "url": "http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/7/",
    "vsphere_service": "vshpere_service",
    "vmname": "vmname"
}

```

### Common Errors

If the CDROM is mounted it, mounting again will unmount it and show status="Failed" and shell_returncode=4.  In this case
repeat the POST to mount it.

```
http POST http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/ state=mount vsphere_service=vshpere_service vmname='vmname' iso_path='[datastore] path/some.iso'
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Connection: close
Content-Length: 487
Content-Type: application/json
Date: Fri, 28 Jul 2017 21:02:25 GMT
Location: http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/4/
Server: gunicorn/19.7.1
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "created": "2017-07-28T21:02:25.193941Z",
    "iso_path": "[datastore] path/some.iso",
    "shell_returncode": 4,
    "state": "mount",
    "status": "Failed",
    "stderr": "Hmm - There was a blocking question.  CDRom is probably unmounted now.\nIf you meant to mount it then try again.\n",
    "stdout": "Searching for VM vmname\n",
    "unit_number": 1,
    "url": "http://127.0.0.1:8000/api/vm-helpers/manage-cdrom/4/",
    "vsphere_service": "vshpere_service",
    "vmname": "vmname"
}

```

Other errors will include using an incorrect iso_path or vmname.

## Openshift: Up and running

```
oc new-project some-project

oc secrets new-sshauth sshsecret --ssh-privatekey=path-to/key

oc secret add serviceaccount/builder secrets/sshsecret

source typical.sh

oc new-app -f openshift/templates/pyvmomi_restapi.yaml \
    --param=DEBUG=${DEBUG} \
    --param=PIP_PROXY=${PIP_PROXY} \
    --param=APPLICATION_DOMAIN=${APPLICATION_DOMAIN} \
    --param=VSPHERE_USERNAME=${VSPHERE_USERNAME} \
    --param=VSPHERE_PASSWORD=${VSPHERE_PASSWORD}
```

####### vi: ai et ts=4 sw=4 sts=4 ru nu filetype=markdown
