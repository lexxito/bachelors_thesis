# -*- encoding: utf-8 -*-
#
# Copyright © 2013 ZHAW SoE
#
# Authors: Serhiienko Oleksii <serh@zhaw.ch>
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

from ceilometer.hardware.pollsters import volt
from ceilometer import sample

from . import base


class TestVoltPollsters(base.TestPollsterBase):
    def test_volt_voltage_current(self):
        self._check_get_samples(volt.VoltVoltagePollster,
                                'volt.voltage.current',
                                0.896, sample.TYPE_GAUGE,
                                volt.VoltVoltagePollster.CACHE_KEY_VOLTAGE)

    def test_rpm_status_current(self):
        self._check_get_samples(volt.VoltStatusPollster,
                                'volt.status.current',
                                "ok", sample.TYPE_GAUGE,
                                volt.VoltStatusPollster.CACHE_KEY_VOLTAGE)
