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

* Copy the file you'd like to modify from the [community samples](https://github.com/vmware/pyvmomi-community-samples/tree/master/samples)
* Update the relevant import statements to point to the sample module, to leverage the features in the community samples
* Add your customization
* Delete the original sample file

```
curl https://raw.githubusercontent.com/vmware/pyvmomi-community-samples/master/samples/get_vm_names.py > get_vm_names.py
cp get_vm_names.py get_vm_names_catch.py

# Add your changes


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

python get_vm_names_catch.py -u '<username>' -s '<vSphere service to connect to>'
```
