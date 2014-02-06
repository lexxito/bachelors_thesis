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

from ceilometer.hardware.pollsters import syslog
from ceilometer import sample

from . import base


class TestSysPollsters(base.TestPollsterBase):
    def test_syslog_date_current(self):
        self._check_get_samples(syslog.LogDatePollster,
                                'syslog.date.event',
                                "27/05/1993 13:49", sample.TYPE_GAUGE,
                                'log')

    def test_syslog_type_current(self):
        self._check_get_samples(syslog.LogTypePollster,
                                'syslog.type.event',
                                "Physical Security #0x51", sample.TYPE_GAUGE,
                                syslog.LogTypePollster.CACHE_KEY_LOG)

    def test_syslog_inter_current(self):
        self._check_get_samples(syslog.LogInterPollster,
                                'syslog.interpretation.event',
                                "General Chassis intrusion", sample.TYPE_GAUGE,
                                syslog.LogInterPollster.CACHE_KEY_LOG)
