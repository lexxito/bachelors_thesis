# -*- encoding: utf-8 -*-
#
# Copyright © 2013 ZHAW SoE
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
"""Tests for ceilometer/hardware/manager
"""

from ceilometer.hardware import inspector
from ceilometer.hardware import manager
from ceilometer import pipeline
from tests import agentbase


class TestRunTasks(agentbase.BaseAgentManagerTestCase):
    def _faux_get_inspector(url, namespace=None):
        return None

    def setup_manager(self):
        self.mgr = manager.AgentManager()
        # stub out before the pipeline is created
        self.stubs.Set(inspector, 'get_inspector', self._faux_get_inspector)

    def test_load_plugins(self):
        self.assertTrue(list(self.mgr.pollster_manager))

    def test_setup_polling_tasks_multiple_resources(self):
        self.pipeline_cfg = [
            {
                'name': "test_pipeline_1",
                'interval': 10,
                'counters': ['test'],
                'resources': ['test://'],
                'transformers': [],
                'publishers': ["test"],
            },
            {
                'name': "test_pipeline_2",
                'interval': 10,
                'counters': ['testanother'],
                'resources': ['test://', 'test2://'],
                'transformers': [],
                'publishers': ["test"],
            },
        ]
        self.mgr.pipeline_manager = pipeline.PipelineManager(
            self.pipeline_cfg,
            self.transformer_manager)
        polling_tasks = self.mgr.setup_polling_tasks()
        self.assertEqual(len(polling_tasks.keys()), 1)
        task = polling_tasks.values()[0]
        self.assertEqual(len(task.host_urls.keys()), 2)
        self.assertTrue('test' in task.host_urls.keys())
        self.assertTrue('testanother' in task.host_urls.keys())
        self.assertEqual(len(task.host_urls['test']), 1)
        self.assertEqual(len(task.host_urls['testanother']), 2)
        # check mgr's loaded driver
        self.assertEqual(len(self.mgr.inspectors.keys()), 2)
        self.assertTrue('test' in self.mgr.inspectors.keys())
        self.assertTrue('test2' in self.mgr.inspectors.keys())

    def test_setup_polling_tasks_none_resources(self):
        self.pipeline_cfg = [
            {
                'name': "test_pipeline_1",
                'interval': 10,
                'counters': ['test'],
                'transformers': [],
                'publishers': ["test"],
            },
        ]
        self.mgr.pipeline_manager = pipeline.PipelineManager(
            self.pipeline_cfg,
            self.transformer_manager)
        polling_tasks = self.mgr.setup_polling_tasks()
        self.assertEqual(len(polling_tasks.keys()), 0)
