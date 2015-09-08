import unittest

import mock
from pulp.agent.lib.report import BindReport, CleanReport

from pulp_puppet.handlers.puppet import BindHandler


class TestBindHandler(unittest.TestCase):
    def setUp(self):
        self.handler = BindHandler({})
        self.conduit = mock.MagicMock()
        self.binding = {'type_id': 'puppet_module', 'repo_id': 'repo1', 'details': {}}

    def test_bind(self):
        # this should be a no-op since we don't store bind state on the consumer
        result = self.handler.bind(self.conduit, self.binding, {})

        self.assertTrue(isinstance(result, BindReport))
        self.assertTrue(result.succeeded)
        self.assertEqual(result.repo_id, self.binding['repo_id'])

    def test_unbind(self):
        # this should be a no-op since we don't store bind state on the consumer
        result = self.handler.unbind(self.conduit, self.binding['repo_id'], {})

        self.assertTrue(isinstance(result, BindReport))
        self.assertTrue(result.succeeded)
        self.assertEqual(result.repo_id, self.binding['repo_id'])

    def test_clean(self):
        # this should be a no-op since we don't store bind state on the consumer
        result = self.handler.clean(self.conduit)

        self.assertTrue(isinstance(result, CleanReport))
        self.assertTrue(result.succeeded)
