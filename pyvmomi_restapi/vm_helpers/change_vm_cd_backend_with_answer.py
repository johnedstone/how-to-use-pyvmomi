#!/usr/bin/env python
#
# Written by JM Lopez
# GitHub: https://github.com/jm66
# Email: jm@jmll.me
# Website: http://jose-manuel.me
#
# Note: Example code For testing purposes only
#
# This code has been released under the terms of the Apache-2.0 license
# http://opensource.org/licenses/Apache-2.0
#
# Updated Jul-2017 by E Johnstone, https://github.com/johnedstone, to deal with unmounting

import atexit
import requests
import sys
from samples.tools import cli
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
from samples.tools import tasks

from time import sleep
import logging
DEBUG = False
if DEBUG:
    logging.basicConfig(level=logging.INFO)

# disable  urllib3 warnings
if hasattr(requests.packages.urllib3, 'disable_warnings'):
    requests.packages.urllib3.disable_warnings()


def update_virtual_cd_backend_by_obj(si, vm_obj, cdrom_number,
                                     content, vm_type,
                                     full_path_to_iso=None):
    """ Updates Virtual Machine CD/DVD backend device
    :param vm_obj: virtual machine object vim.VirtualMachine
    :param cdrom_number: CD/DVD drive unit number
    :param si: Service Instance
    :param full_path_to_iso: Full path to iso
    :return: True or false in case of success or error
    """

    cdrom_prefix_label = 'CD/DVD drive '
    cdrom_label = cdrom_prefix_label + str(cdrom_number)
    virtual_cdrom_device = None
    for dev in vm_obj.config.hardware.device:
        if isinstance(dev, vim.vm.device.VirtualCdrom) \
                and dev.deviceInfo.label == cdrom_label:
            virtual_cdrom_device = dev

    if not virtual_cdrom_device:
        raise RuntimeError('Virtual {} could not '
                           'be found.'.format(cdrom_label))

    virtual_cd_spec = vim.vm.device.VirtualDeviceSpec()
    virtual_cd_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
    virtual_cd_spec.device = vim.vm.device.VirtualCdrom()
    virtual_cd_spec.device.controllerKey = virtual_cdrom_device.controllerKey
    virtual_cd_spec.device.key = virtual_cdrom_device.key
    virtual_cd_spec.device.connectable = \
        vim.vm.device.VirtualDevice.ConnectInfo()
    # if full_path_to_iso is provided it will mount the iso
    if full_path_to_iso:
        virtual_cd_spec.device.backing = \
            vim.vm.device.VirtualCdrom.IsoBackingInfo()
        virtual_cd_spec.device.backing.fileName = full_path_to_iso
        virtual_cd_spec.device.connectable.connected = True
        virtual_cd_spec.device.connectable.startConnected = True
    else:
        virtual_cd_spec.device.backing = \
            vim.vm.device.VirtualCdrom.RemotePassthroughBackingInfo()
    # Allowing guest control
    virtual_cd_spec.device.connectable.allowGuestControl = True

    dev_changes = []
    dev_changes.append(virtual_cd_spec)
    spec = vim.vm.ConfigSpec()
    spec.deviceChange = dev_changes
    task = vm_obj.ReconfigVM_Task(spec=spec)

    # Look for blocking question
    # Ref: http://www.lucd.info/2015/10/02/answer-the-question/
    # This loop is in place of vm_obj.UpdateViewData('runtime.question') which is in PowerCLI
    #     but I can't find in pyvmomi

    logging.info("Checking for the Guest Control Question")
    for n in range(5):
        logging.info('interation: {}'.format(n))
        vm_obj_refresh = get_obj(content, vm_type, vm_obj.name)
        logging.info('vm_obj_refresh: {}'.format(vm_obj_refresh))
        if vm_obj_refresh:
            question = vm_obj_refresh.runtime.question
            logging.info('vm_obj_refresh.runtime.question: {}'.format(vm_obj_refresh.runtime.question))
            if question and 'The guest operating system has locked the CD-ROM door' in question.text:
                logging.info('Do the unlocking here')
                # See https://github.com/vmware/pyvmomi-community-samples/blob/master/samples/virtual_machine_power_cycle_and_question.py
                vm_obj_refresh.AnswerVM(question.id, '0')
                if full_path_to_iso:
                    sys.stderr.write("Hmm - There was a blocking question.  CDRom is probably unmounted now.\nIf you meant to mount it then try again.\n") 
                    sys.exit(4)
                else:
                    sys.stdout.write("The Question has been answered 'Yes'. The CDRom is disconnected\n") 

                break
        sleep(1)

    tasks.wait_for_tasks(si, [task])
    return True


def get_args():
    parser = cli.build_arg_parser()
    parser.add_argument('-n', '--vmname', required=True,
                        help="Name of the VirtualMachine you want to change.")
    parser.add_argument('-m', '--unitnumber', required=True,
                        help='CD/DVD unit number.', type=int)
    parser.add_argument('-i', '--iso', required=False,
                        help='Full path to iso. i.e. "[ds1] folder/Ubuntu.iso"'
                             ' If not provided, backend will'
                             ' set to RemotePassThrough')
    my_args = parser.parse_args()
    return cli.prompt_for_password(my_args)


def get_obj(content, vim_type, name):
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vim_type, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def main():
    args = get_args()

    # connect to vc
    si = SmartConnect(
        host=args.host,
        user=args.user,
        pwd=args.password,
        port=args.port)
    # disconnect vc
    atexit.register(Disconnect, si)

    content = si.RetrieveContent()
    print 'Searching for VM {}'.format(args.vmname)
    vm_obj = get_obj(content, [vim.VirtualMachine], args.vmname)

    if vm_obj:
        update_virtual_cd_backend_by_obj(si, vm_obj, args.unitnumber,
                                         content, [vim.VirtualMachine], args.iso)
        device_change = args.iso if args.iso else 'Client Device'
        print 'VM CD/DVD {} successfully' \
              ' state changed to {}'.format(args.unitnumber, device_change)
    else:
        print "VM not found"

# start
if __name__ == "__main__":
    main()

# vi: ai et ts=4 sw=4 sts=4 ru nu
