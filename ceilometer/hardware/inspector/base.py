# -*- encoding: utf-8 -*-
#
# Copyright © 2014 ZHAW SoE
#
# Authors: Lucas Graf <graflu0@students.zhaw.ch>
#          Toni Zehnder <zehndton@students.zhaw.ch>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
"""Inspector abstraction for read-only access to hardware components"""

import abc
import collections

import six

# Named tuple representing CPU statistics.
#
# cpu1MinLoad: 1 minute load
# cpu5MinLoad: 5 minute load
# cpu15MinLoad: 15 minute load
#
CPUStats = collections.namedtuple(
    'CPUStats',
    ['cpu_1_min', 'cpu_5_min', 'cpu_15_min'])

# Named tuple representing RAM statistics.
#
# total: Total Memory (bytes)
# used: Used Memory (bytes)
#
MemoryStats = collections.namedtuple('MemoryStats', ['total', 'used'])

# Named tuple representing disks.
#
# device: the device name for the disk
# path: the path from the disk
#
Disk = collections.namedtuple('Disk', ['device', 'path'])

# Named tuple representing disk statistics.
#
# size: storage size (bytes)
# used: storage used (bytes)
#
DiskStats = collections.namedtuple('DiskStats', ['size', 'used'])


# Named tuple representing an interface.
#
# name: the name of the interface
# mac: the MAC of the interface
# ip: the IP of the interface
#
Interface = collections.namedtuple('Interface', ['name', 'mac', 'ip'])


# Named tuple representing network interface statistics.
#
# bandwidth: current bandwidth (bytes/s)
# rx_bytes: total number of octets received (bytes)
# tx_bytes: total number of octets transmitted (bytes)
# error: number of outbound packets not transmitted because of errors
#
InterfaceStats = collections.namedtuple(
    'InterfaceStats',
    ['bandwidth', 'rx_bytes', 'tx_bytes', 'error'])

# Named tuple representing an Fan.
#
# name: the name of the fan
#
RPM = collections.namedtuple('RPM', ['name'])


# Named tuple representing Fan statistics.
#
# speed: current speed(RPM)
# status: state of fan (ok)
#
RPMStats = collections.namedtuple('RPMStats', ['speed', 'status'])


# Named tuple representing an voltage.
#
# name: the name of the system element
#
Volt = collections.namedtuple('Volt', ['name'])


# Named tuple representing voltage statistics.
#
# voltage: current voltage(Volt)
# status: state of element (ok)
#
VoltStats = collections.namedtuple('VoltStats', ['voltage', 'status'])


# Named tuple representing an temperature.
#
# name: the name of the system element
#
Degree = collections.namedtuple('Degree', ['name'])


# Named tuple representing network temperature statistics.
#
# temperature: current temperature(Degree C)
# status: state of element (ok)
#
DegreeStats = collections.namedtuple('DegreeStats', ['temperature', 'status'])


# Named tuple representing system log's statistics.
#
# number: current number of log
#


@six.add_metaclass(abc.ABCMeta)
class Inspector(object):
    @abc.abstractmethod
    def inspect_cpu(self, host):
        """Inspect the CPU statistics for a host.

        :param host: the target host
        :return: iterator of CPUStats
        """

    @abc.abstractmethod
    def inspect_disk(self, host):
        """Inspect the disk statistics for a host.

        :param : the target host
        :return: iterator of tuple (Disk, DiskStats)
        """

    @abc.abstractmethod
    def inspect_memory(self, host):
        """Inspect the ram statistics for a host.

        :param : the target host
        :return: iterator of MemoryStats
        """

    @abc.abstractmethod
    def inspect_network(self, host):
        """Inspect the network interfaces for a host.

        :param : the target host
        :return: iterator of tuple (Interface, InterfaceStats)
        """

@six.add_metaclass(abc.ABCMeta)
class InspectorIPMI(object):
    @abc.abstractmethod
    def inspect_speed(self, host):
        """Inspect the fan's speed for a host.

        param : the target host
        :return: iterator of tuple (RPM, RPMStats)
        """

    @abc.abstractmethod
    def inspect_voltage(self, host):
        """Inspect the element's voltage for a host.

        :param : the target host
        :return: iterator of tuple (Volt, VoltStats)
        """

    @abc.abstractmethod
    def inspect_temperature(self, host):
        """Inspect the element's temperature for a host.

        :param : the target host
        :return: iterator of tuple (Degree, DegreeStats)
        """