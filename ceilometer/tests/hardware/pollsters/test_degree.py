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

from ceilometer.hardware.pollsters import degree
from ceilometer import sample
from ceilometer.tests.hardware.pollsters import base


class TestDegreePollsters(base.TestPollsterBase):
    def test_degree_temperature_current(self):
        self._check_get_samples(degree.DegreeTemperaturePollster,
                                'degree.temperature.current',
                                30, sample.TYPE_CUMULATIVE)

    def test_degree_status_current(self):
        self._check_get_samples(degree.DegreeStatusPollster,
                                'degree.status.current',
                                "ok", sample.TYPE_CUMULATIVE)
