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
"""Tests for ceilometer/hardware/inspector/snmp/inspector.py
"""


from ceilometer.hardware.inspector import ipmi
from ceilometer.openstack.common import network_utils
from ceilometer.tests import base as test_base
from ceilometer.tests.hardware.inspector import base

BaseIPMI = base.InspectorBaseTestIPMI

fake_sensor_output = (BaseIPMI.rpm[0][0].name + "|"
                      + str(BaseIPMI.rpm[0][1].speed) + "|"
                      + "RPM" + "|"
                      + BaseIPMI.rpm[0][1].status) + "|" + "\n" + \
                     (BaseIPMI.rpm[1][0].name + "|"
                      + str(BaseIPMI.rpm[1][1].speed) + "|"
                      + "RPM" + "|" + BaseIPMI.rpm[1][1].status) + "|" + "\n"
fake_sensor_output += (BaseIPMI.volt[0][0].name + "|"
                       + str(BaseIPMI.volt[0][1].voltage) + "|"
                       + "Volts" + "|" + BaseIPMI.volt[0][1].status) + "\n" + \
                      (BaseIPMI.volt[1][0].name + "|"
                       + str(BaseIPMI.volt[1][1].voltage) + "|"
                       + "Volts" + "|" + BaseIPMI.volt[1][1].status) + "\n"
fake_sensor_output += (BaseIPMI.degree[0][0].name + "|"
                       + str(BaseIPMI.degree[0][1].temperature) + "|"
                       + "degrees C" + "|"
                       + BaseIPMI.degree[0][1].status) + "\n" + \
                      (BaseIPMI.degree[1][0].name + "|"
                       + str(BaseIPMI.degree[1][1].temperature) + "|"
                       + "degrees C" + "|"
                       + BaseIPMI.degree[1][1].status) + "\n"


def fake_sensor_list(autoHost):
    return fake_sensor_output


class TestIPMIInspector(BaseIPMI, test_base.BaseTestCase):
    def setUp(self):
        super(TestIPMIInspector, self).setUp()
        self.inspector = ipmi.IPMIInspector()
        self.host = network_utils.urlsplit("ipmi://ADMIN:ADMIN@160.85.197.44")
        self.stubs.Set(self.inspector,
                       'execute_sensor_ipmi_command',
                       fake_sensor_list)
