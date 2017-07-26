## Description

The two python VMWare projects are well documented and have many good examples: [pyvmomi](https://github.com/vmware/pyvmomi), [pyvmomi-community-samples](https://github.com/vmware/pyvmomi-community-samples).  This repository describes how these to use these two projects, along with an example of a [python REST API](http://www.django-rest-framework.org/) that can be used as a wrapper for others to consume.

## Setup
*Note: use python virtualenvs* 

```
pip install pip --upgrade
pip install -r requirements.txt
```

## Leveraging the Pyvmomi Community Samples
In the example below, the following steps are demonstratned

* Copy the file to be modified from the [community samples](https://github.com/vmware/pyvmomi-community-samples/tree/master/samples)
* Update the relevant import statements to point to the sample module, to leverage the features in the community samples
* Add other customizations
* Delete the original sample file

```
curl -s https://raw.githubusercontent.com/vmware/pyvmomi-community-samples/master/samples/get_vm_names.py > get_vm_names.py
cp get_vm_names.py get_vm_names_catch.py

# Update the import statemens and add customization

diff -u get_vm_names.py get_vm_names_catch.py
--- get_vm_names.py     2017-07-25 23:51:08.000192000 -0400
+++ get_vm_names_catch.py       2017-07-25 23:51:22.000011000 -0400
@@ -19,7 +19,12 @@
 import atexit
 from pyVim.connect import SmartConnectNoSSL, Disconnect
 from pyVmomi import vim
-from tools import cli
+from samples.tools import cli
+
+import logging
+DEBUG = True
+if DEBUG:
+    logging.basicConfig(level=logging.INFO)

 MAX_DEPTH = 10

@@ -52,7 +57,11 @@
         return

     summary = vm.summary
-    print(summary.config.name)
+    try:
+        print('{}|{}'.format(summary.config.name, vm.name))
+    except AttributeError as e:
+        print('{}|{}'.format('unknown', vm.name))
+        logging.error(e)


 def main():
@@ -84,3 +93,5 @@
 # Start program
 if __name__ == "__main__":
     main()
+
+# vi: ai et ts=4 sts=4 sw=4 ru nu

rm get_vm_names.py

# Test the new script
python get_vm_names_catch.py -u '<username>' -s '<vSphere service to connect to>'
```

The second example customizes the mount/umount CDROM ISO script, in order to handle question that is waiting for a response.

```
curl -s https://raw.githubusercontent.com/vmware/pyvmomi-community-samples/master/samples/change_vm_cd_backend.py > change_vm_cd_backend.py

cp change_vm_cd_backend.py change_vm_cd_backend_with_answer.py

# Update the import statements and add customization

diff -u change_vm_cd_backend.py change_vm_cd_backend_with_answer.py
--- change_vm_cd_backend.py     2017-07-26 00:09:20.000195000 -0400
+++ change_vm_cd_backend_with_answer.py 2017-07-26 00:10:57.000004000 -0400
@@ -10,13 +10,20 @@
 # This code has been released under the terms of the Apache-2.0 license
 # http://opensource.org/licenses/Apache-2.0
 #
+# Updated Jul-2017 by E Johnstone, https://github.com/johnedstone, to deal with unmounting

 import atexit
 import requests
-from tools import cli
+from samples.tools import cli
 from pyVmomi import vim
 from pyVim.connect import SmartConnect, Disconnect
-from tools import tasks
+from samples.tools import tasks
+
+from time import sleep
+import logging
+DEBUG = True
+if DEBUG:
+    logging.basicConfig(level=logging.INFO)

 # disable  urllib3 warnings
 if hasattr(requests.packages.urllib3, 'disable_warnings'):
@@ -24,6 +31,7 @@


 def update_virtual_cd_backend_by_obj(si, vm_obj, cdrom_number,
+                                     content, vm_type,
                                      full_path_to_iso=None):
     """ Updates Virtual Machine CD/DVD backend device
     :param vm_obj: virtual machine object vim.VirtualMachine
@@ -70,6 +78,24 @@
     spec = vim.vm.ConfigSpec()
     spec.deviceChange = dev_changes
     task = vm_obj.ReconfigVM_Task(spec=spec)
+
+    # Look for blocking question
+    # Ref: http://www.lucd.info/2015/10/02/answer-the-question/
+    if not full_path_to_iso:
+      for n in range(5):
+        logging.info('interation: {}'.format(n))
+        vm_obj_refresh = get_obj(content, vm_type, vm_obj.name)
+        logging.info('vm_obj_refresh: {}'.format(vm_obj_refresh))
+        if vm_obj_refresh:
+            question = vm_obj_refresh.runtime.question
+            logging.info('vm_obj_refresh.runtime.question: {}'.format(vm_obj_refresh.runtime.question))
+            if question and 'The guest operating system has locked the CD-ROM door' in question.text:
+                logging.info('Do the unlocking here')
+                # See https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/virtual_machine_power_cycle_and_question.py
+                vm_obj_refresh.AnswerVM(question.id, '0')
+                break
+        sleep(1)
+
     tasks.wait_for_tasks(si, [task])
     return True

@@ -116,7 +142,8 @@
     vm_obj = get_obj(content, [vim.VirtualMachine], args.vmname)

     if vm_obj:
-        update_virtual_cd_backend_by_obj(si, vm_obj, args.unitnumber, args.iso)
+        update_virtual_cd_backend_by_obj(si, vm_obj, args.unitnumber,
+                                         content, [vim.VirtualMachine], args.iso)
         device_change = args.iso if args.iso else 'Client Device'
         print 'VM CD/DVD {} successfully' \
               ' state changed to {}'.format(args.unitnumber, device_change)
@@ -126,3 +153,5 @@
 # start
 if __name__ == "__main__":
     main()
+
+# vi: ai et ts=4 sw=4 sts=4 ru nu

rm change_vm_cd_backend.py

python change_vm_cd_backend_with_answer.py -u 'username' -s '<vSphere service to connect to>' -n '<VMNAME>' -m 1 -i '[datastore] path-to-iso'
Searching for VM VMNAME
VM CD/DVD 1 successfully state changed to [datastore] path-to-iso 

# Umount the iso
python change_vm_cd_backend_with_answer.py -u 'username' -s '<vSphere service to connect to>' -n '<VMNAME>'' -m 1
Searching for VM VMName
INFO:root:Do the unlocking here
VM CD/DVD 1 successfully state changed to Client Device

```
