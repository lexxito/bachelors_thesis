# -*- encoding: utf-8 -*-
#
# Copyright © 2013 Intel Corp
#
# Authors: Lianhao Lu <lianhao.lu@intel.com>
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

from ceilometer.hardware.inspector import base


class InspectorBaseTest(object):
    """Subclass must set self.inspector and self.host in
    self.setUp()
    """

    cpu = [base.CPUStats(cpu1MinLoad=0.1,
                         cpu5MinLoad=0.2,
                         cpu15MinLoad=0.3),
           ]

    network = [(base.Interface(name='eth0',
                               mac='112233445566',
                               ip='10.0.0.1'),
                base.InterfaceStats(bandwidth=1250000 / 8,
                                    rx_bytes=1000,
                                    tx_bytes=2000,
                                    error=1)),
               ]
    diskspace = [(base.Disk(device='/dev/sda1', path='/'),
                  base.DiskStats(size=1000, used=500),
                  ),
                 (base.Disk(device='/dev/sda2', path='/home'),
                  base.DiskStats(size=2000, used=1000),
                  ),
                 ]
    memory = [base.MemoryStats(total=1000, used=500)]

    def test_inspect_cpu(self):
        self.assertEqual(list(self.inspector.inspect_cpu(self.host)),
                         self.cpu)

    def test_inspect_network(self):
        self.assertEqual(list(self.inspector.inspect_network(self.host)),
                         self.network)

    def test_inspect_diskspace(self):
        self.assertEqual(list(self.inspector.inspect_diskspace(self.host)),
                         self.diskspace)

    def test_inspect_memory(self):
        self.assertEqual(list(self.inspector.inspect_memoryspace(self.host)),
                         self.memory)


class InspectorBaseTestIPMI(object):
    """Subclass must set self.inspector and self.host in
    self.setUp()
    """

    rpm = [(base.RPM(name="FAN 1"),
            base.RPMStats(speed=14985.0, status='ok')
            ),
           (base.RPM(name="FAN 2"),
            base.RPMStats(speed=16788.0, status='ok')
            ),

           ]
    degree = [(base.Degree(name="System Temp"),
               base.DegreeStats(temperature=33.0, status='ok')
               ),
              (base.Degree(name="CPU Temp"),
               base.DegreeStats(temperature=48.0, status='ok')
               ),
              ]
    volt = [(base.Volt(name="Vcore"),
            base.VoltStats(voltage=1.23, status='ok'),
             ),
            (base.Volt(name="12V"),
            base.VoltStats(voltage=12.4, status='ok'),
             ),
            ]
    syslog = [(base.SysLog(number="1"),
               base.SysLogStats(date='01/31/2012 16:37:04',
                                log_type='Physical Security #0x51',
                                interpretation='General Chassis intrusion'),
               ),
              (base.SysLog(number="8"),
               base.SysLogStats(date='09/16/2013 11:37:35',
                                log_type='Processor #0x61',
                                interpretation='Disabled'),
               ),
              ]

    def test_inspect_speed(self):
        self.assertEqual(list(self.inspector.inspect_speed(self.host)),
                         self.rpm)

    def test_inspect_temperature(self):
        self.assertEqual(list(self.inspector.inspect_temperature(self.host)),
                         self.degree)

    def test_inspect_voltage(self):
        self.assertEqual(list(self.inspector.inspect_voltage(self.host)),
                         self.volt)

    def test_inspect_syslog(self):
        self.assertEqual(list(self.inspector.inspect_sys_logs(self.host)),
                         self.syslog)
