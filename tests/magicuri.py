#!/usr/bin/env python3

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from virtinst import URI


def parse_options():
    description = ("Generate a fake URI for use with virt-manager/virtinst "
        "that wraps a standard test:/// URI but pretends to be a different "
        "hypervisor. See virtinst/uri.py MagicURI for format details. "
        "Example: magicuri.py qemu+tcp://fakeuri.example.com/system")
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("fakeuri",
            help="The libvirt URI we should fake")
    parser.add_argument("--capsfile",
            help="Path to file to use for capabilities XML")
    parser.add_argument("--domcapsfile",
            help="Path to file to use for domain capabilities XML")
    parser.add_argument("--driverxml",
            help="Path to driver xml (defaults to testdriver.xml)")

    options = parser.parse_args()

    testdir = os.path.abspath(os.path.dirname(__file__))
    capsdir = os.path.join(testdir, "data/capabilities/")

    uriobj = URI(options.fakeuri)
    hv = uriobj.scheme

    capsfile = None
    domcapsfile = None
    if hv == "lxc":
        capsfile = f"{capsdir}lxc.xml"
    elif hv == "qemu":
        capsfile = f"{capsdir}kvm-x86_64.xml"
        domcapsfile = f"{capsdir}kvm-x86_64-domcaps.xml"
    elif hv == "vz":
        capsfile = f"{capsdir}vz.xml"

    elif hv == "xen":
        capsfile = f"{capsdir}xen-rhel5.4.xml"
    if options.capsfile:
        capsfile = os.path.abspath(options.capsfile)
    if options.domcapsfile:
        domcapsfile = os.path.abspath(options.domcapsfile)

    driverxml = os.path.join(testdir, "testdriver.xml")
    if options.driverxml:
        driverxml = os.path.abspath(options.driverxml)

    return options.fakeuri, capsfile, domcapsfile, driverxml


def main():
    fakeuri, capsfile, domcapsfile, driverxml = parse_options()
    uri = f"__virtinst_test__test://{driverxml}"
    uri += f",fakeuri={fakeuri}"

    if capsfile:
        uri += f",caps={capsfile}"
    if domcapsfile:
        uri += f",domcaps={domcapsfile}"

    if driverxml and not os.path.exists(driverxml):
        print(f"{capsfile} does not exist")
        return 1
    if capsfile and not os.path.exists(capsfile):
        print(f"{capsfile} does not exist")
        return 1
    if domcapsfile and not os.path.exists(domcapsfile):
        print(f"{domcapsfile} does not exist")
        return 1

    print(uri)
    return 0

if __name__ == "__main__":
    sys.exit(main())
