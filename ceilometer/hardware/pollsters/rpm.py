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

from ceilometer.hardware import plugin
from ceilometer.hardware.pollsters import util
from ceilometer import sample


class _Base(plugin.HardwarePollster):

    CACHE_KEY = 'rpm'
    INSPECT_METHOD = 'inspect_speed'


class RPMSpeedPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (rpm, info) = c_data
        return util.make_sample_from_host(host,
                                          name='rpm.speed.current',
                                          type=sample.TYPE_GAUGE,
                                          unit='B',
                                          volume=info.speed,
                                          res_metadata=rpm,
                                          )


class RPMStatusPollster(_Base):

    @staticmethod
    def generate_one_sample(host, c_data):
        (rpm, info) = c_data
        return util.make_sample_from_host(host,
                                          name='rpm.status.current',
                                          type=sample.TYPE_GAUGE,
                                          unit='B',
                                          volume=info.status,
                                          res_metadata=rpm,
                                          )
