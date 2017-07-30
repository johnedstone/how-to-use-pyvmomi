## Description

The scripts in the custom_scripts directory in this repository can be
exposed as REST API endpoints.  This project describes an example using
the [Django Rest Framework](http://www.django-rest-framework.org/).  This django
project is written for PaaS, specifically Openshift.  But it can be adapted on
any platform that Django runs on.

## Quick Summary
Once this REST API is implemented in Openshift, the following examples show mounting and
umounting an ISO in the CDROM.

* Note: Larger vCenters have longer response times.  In this case, increase the parameters PVMOMI_TIMEOUT
and/or ITERATIONS_WAITING_FOR_BLOCKING_QUESTION.  The defaults are 240 sec and 3 iterations. This timeout
is the time allowed before killing the internal call to vSphere. The iterations are looking for the
blocking question, that appears in the UI, waiting to answer 'yes'.

* The `--timeout 300` in the examples below sets the client to wait 5 min for a responce.  Internally,
for Openshift, in the file `.s2i/bin/run`, gunicorn is set to timeout 10 min.

* In the example below [HTTPie](https://httpie.org/) is used in place of curl.

```
http --timeout 300 POST https://FQDN/api/vm-helpers/manage-cdrom/ state=mount vmname='vmname' vsphere_service='vsphere_service' iso_path='[datastore] path/some.iso'
http --timeout 300 POST https://FQDN/api/vm-helpers/manage-cdrom/ state=umount vmname='vmname' vsphere_service='vsphere_service'
```

* These same commands, executed with curl, are listed here.

```
curl -k -X POST -H "Content-Type: application/json" -d '{"state": "mount", "vmname": "vmname", "vsphere_service": "vsphere_service",  "iso_path": "[datastore] path/some.iso"}' https://FQDN/api/vm-helpers/manage-cdrom/
curl -k -X POST -H "Content-Type: application/json" -d '{"state": "umount", "vmname": "vmname", "vsphere_service": "vsphere_service"}' https://FQDN/api/vm-helpers/manage-cdrom/
```

## Setup
```
cd pyvmomi_restapi
pip install requirements.txt
python manage.py migrate

# Develop/Debug
export DEBUG=on SPHERE_USERNAME='someusername' VSPHERE_PASSWORD='somepassword'
python manage.py runserver
```

## Swagger (documentation)
URL for documentation with Swagger: /swagger/

## Usage
Note: in these examples the python project [HTTPie](https://httpie.org/) is used in place of curl

### What is success?
A `mount` or `umount`, to be successful will return two fields:

* shell_returncode: 0
* status: Success

If these two fields are not displayed with 0 and Success, respectively
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

If the CDROM is already mounted it, in some cases, mounting it again will unmount it and show status="Failed" and shell_returncode=4.  In this case
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

Here is an error where there is a successful umount, yet there is a vim.fault.GenericVmConfigFault

```
time http --timeout 300 POST https://FQDN/api/vm-helpers/manage-cdrom/ state=umount vmname='vmname' vsphere_service=vsphere_service
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 1230
Content-Type: application/json
Date: Sat, 29 Jul 2017 07:27:02 GMT
Location: https://FQDM/api/vm-helpers/manage-cdrom/4/
Server: gunicorn/19.7.1
Set-Cookie: 5b992246cb8ec8e2ffa72e32820fea5d=56285f5d04fc2e8e5017d2469ad746fd; path=/; HttpOnly; Secure
X-Frame-Options: SAMEORIGIN

{
    "created": "2017-07-29T07:27:02.296155Z",
    "iso_path": "",
    "shell_returncode": 0,
    "state": "umount",
    "status": "Success",
    "stderr": "ERROR:root:update_virtual_cd_backend_by_obj Exception: (vim.fault.GenericVmConfigFault) {\n   dynamicType = <unset>,\n   dynamicProperty = (vmodl.DynamicProperty) [],\n   msg = \"Device 'ide0:0' already exists.\",\n   faultCause = <unset>,\n   faultMessage = (vmodl.LocalizableMessage) [\n      (vmodl.LocalizableMessage) {\n         dynamicType = <unset>,\n         dynamicProperty = (vmodl.DynamicProperty) [],\n         key = 'msg.disk.alreadyExists',\n         arg = (vmodl.KeyAnyValue) [\n            (vmodl.KeyAnyValue) {\n               dynamicType = <unset>,\n               dynamicProperty = (vmodl.DynamicProperty) [],\n               key = '1',\n               value = 'ide0:0'\n            }\n         ],\n         message = \"Device 'ide0:0' already exists.\"\n      }\n   ],\n   reason = \"Device 'ide0:0' already exists.\"\n}\n",
    "stdout": "Searching for VM vmname\nVM CD/DVD 1 successfully state changed to Client Device\n",
    "unit_number": 1,
    "url": "https://FQDN/api/vm-helpers/manage-cdrom/4/",
    "vmname": "vmname",
    "vsphere_service": "vsphere_service"
}


real    2m36.955s
user    0m0.252s
sys     0m0.145s

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
    --param=VSPHERE_PASSWORD=${VSPHERE_PASSWORD} \
    --param=PVMOMI_TIMEOUT=${PVMOMI_TIMEOUT} \
    --param=ITERATIONS_WAITING_FOR_BLOCKING_QUESTION=${ITERATIONS_WAITING_FOR_BLOCKING_QUESTION}
```

