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

import mock

from ceilometer.hardware import inspector
from ceilometer.hardware.inspector import base as inspector_base
from ceilometer.hardware import manager
from ceilometer.openstack.common import network_utils
from ceilometer.tests import base as test_base


class FakeInspector(inspector_base.Inspector):
    CPU = inspector_base.CPUStats(cpu1MinLoad=0.99,
                                  cpu5MinLoad=0.77,
                                  cpu15MinLoad=0.55)
    DISK = (inspector_base.Disk(device='/dev/sda1', path='/'),
            inspector_base.DiskStats(size=1000, used=90))
    MEMORY = inspector_base.MemoryStats(total=1000, used=90)
    NET = (inspector_base.Interface(name='test.teest',
                                    mac='001122334455',
                                    ip='10.0.0.2'),
           inspector_base.InterfaceStats(bandwidth=1000,
                                         rx_bytes=90,
                                         tx_bytes=80,
                                         error=1))
    RPM = (inspector_base.RPM(name="FAN"),
           inspector_base.RPMStats(speed=1470,
                                   status="ok"))
    VOLT = (inspector_base.Volt(name="Vcore"),
            inspector_base.VoltStats(voltage=0.896,
                                     status="ok"))
    DEGREE = (inspector_base.Degree(name="System Temp"),
              inspector_base.DegreeStats(temperature=30.000,
                                         status="ok"))
    SYS_LOG = (inspector_base.SysLog(number='1'),
               inspector_base.SysLogStats(date='27/05/1993 13:49',
                                          log_type="Physical Security #0x51",
                                          interpretation=
                                          "General Chassis intrusion"))

    def inspect_cpu(self, host):
        yield self.CPU

    def inspect_diskspace(self, host):
        yield self.DISK

    def inspect_memoryspace(self, host):
        yield self.MEMORY

    def inspect_network(self, host):
        yield self.NET

    def inspect_speed(self, host):
        yield self.RPM

    def inspect_voltage(self, host):
        yield self.VOLT

    def inspect_temperature(self, host):
        yield self.DEGREE

    def inspect_sys_logs(self, host):
        yield self.SYS_LOG


class TestPollsterBase(test_base.TestCase):
    def faux_get_inspector(url, namespace=None):
        return FakeInspector()

    def setUp(self):
        super(TestPollsterBase, self).setUp()
        self.host = network_utils.urlsplit("test://test")
        self.stubs.Set(inspector, 'get_inspector', self.faux_get_inspector)

    @mock.patch('ceilometer.pipeline.setup_pipeline', mock.MagicMock())
    def _check_get_samples(self, factory, name,
                           expected_value, expected_type,
                           cache_key):
        mgr = manager.AgentManager()
        mgr.load_inspector(self.host)
        pollster = factory()
        cache = {}
        samples = list(pollster.get_samples(mgr, cache, self.host))
        self.assertTrue(samples)
        self.assertTrue(cache_key in cache)
        self.assertTrue(self.host.hostname in cache[cache_key])

        self.assertEqual(set([s.name for s in samples]),
                         set([name]))
        match = [s for s in samples if s.name == name]
        self.assertEqual(match[0].volume, expected_value)
        self.assertEqual(match[0].type, expected_type)
