# -*- encoding: utf-8 -*-
#
# Copyright © 2013 ZHAW SoE
#
# Author: Serhiienko Oleksii<serh@zhaw.ch>
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
"""Inspector for collecting data over IPMI"""

from ceilometer.hardware.inspector import base
from ceilometer.openstack.common import log as logging
import subprocess

LOG = logging.getLogger(__name__)


class IPMIException(Exception):
    pass


class IPMIInspector(base.InspectorIPMI):

    def __init__(self):
        super(IPMIInspector, self).__init__()

    def execute_ipmi_command(self, host, command):
        hostname = host.hostname
        password = host.netloc.split(":")[1].split("@")[0]
        user = host.netloc.split(":")[0]
        all_command = "ipmitool "
        all_command += command
        all_command += " -H " + hostname
        all_command += " -U " + user
        all_command += " -P " + password
        child = subprocess.Popen(all_command,
                                 shell=True,
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        output, error = child.communicate()
        if child.returncode == 0:
            return output
        else:

            LOG.error(error)
        raise IPMIException

    def execute_sensor_ipmi_command(self, host):
        return self.execute_ipmi_command(host, "sensor")

    def execute_syslog_ipmi_command(self, host):
        return self.execute_ipmi_command(host, "sel list")

    def get_sensor_list(self, host, sensor):
        sensor_list = []
        output = self.execute_sensor_ipmi_command(host)
        for line in output.split('\n'):
            if line:
                if line.split('|')[2].strip() == sensor:
                    sensor_list.append({
                        "name": line.split('|')[0].strip(),
                        "value": float(line.split('|')[1].strip()),
                        "status": line.split('|')[3].strip()
                    })
        if not sensor_list:
            LOG.error("No %s sensor", sensor)
        else:
            return sensor_list

    def inspect_speed(self, host):


        sensor_list = self.get_sensor_list(host, "RPM")
        for sensor in sensor_list:
            rpm = base.RPM(name=sensor["name"])
            stats = base.RPMStats(speed=sensor["value"],
                                  status=sensor["status"])
            yield (rpm, stats)

    def inspect_voltage(self, host):
        sensor_list = self.get_sensor_list(host, "Volts")
        for sensor in sensor_list:
            volt = base.Volt(name=sensor["name"])
            stats = base.VoltStats(voltage=sensor["value"],
                                   status=sensor["status"])
            yield (volt, stats)

    def inspect_temperature(self, host):
        sensor_list = self.get_sensor_list(host, "degrees C")
        for sensor in sensor_list:
            degree = base.Degree(name=sensor["name"])
            stats = base.DegreeStats(temperature=sensor["value"],
                                     status=sensor["status"])
            yield (degree, stats)