#!/usr/bin/env python
# See COPYRIGHT file at the top of the source tree.
from __future__ import print_function
from builtins import zip

import os
import unittest

import yaml
import astropy.units as u

from lsst.validate.base import Metric, Datum


class MetricTestCase(unittest.TestCase):
    """Test Metrics and metrics.yaml functionality."""

    def setUp(self):
        yaml_path = os.path.join(os.path.dirname(__file__),
                                 'data', 'metrics.yaml')
        with open(yaml_path) as f:
            self.metric_doc = yaml.load(f)

    def tearDown(self):
        pass

    def test_load_all_yaml_metrics(self):
        """Verify that all metrics from metrics.yaml can be loaded."""
        for metric_name in self.metric_doc:
            m = Metric.from_yaml(metric_name, yaml_doc=self.metric_doc)
            self.assertIsInstance(m, Metric)

    def test_reference_string(self):
        """Verify reference property for different reference datasets."""
        m1 = Metric('test', 'test', '<=', reference_url='example.com',
                    reference_doc='Doc', reference_page=1)
        self.assertEqual(m1.reference, 'Doc, p. 1, example.com')

        m2 = Metric('test', 'test', '<=', reference_url='example.com')
        self.assertEqual(m2.reference, 'example.com')

        m3 = Metric('test', 'test', '<=', reference_url='example.com',
                    reference_doc='Doc')
        self.assertEqual(m3.reference, 'Doc, example.com')

        m4 = Metric('test', 'test', '<=',
                    reference_doc='Doc', reference_page=1)
        self.assertEqual(m4.reference, 'Doc, p. 1')

        m4 = Metric('test', 'test', '<=',
                    reference_doc='Doc')
        self.assertEqual(m4.reference, 'Doc')

    def test_operator_conversion(self):
        """Tests for Metric.convert_operator_str."""
        self.assertTrue(Metric.convert_operator_str('>=')(7, 7))
        self.assertTrue(Metric.convert_operator_str('>')(7, 5))
        self.assertTrue(Metric.convert_operator_str('<')(5, 7))
        self.assertTrue(Metric.convert_operator_str('<=')(7, 7))
        self.assertTrue(Metric.convert_operator_str('==')(7, 7))
        self.assertTrue(Metric.convert_operator_str('!=')(7, 5))

    def test_json(self):
        """Simple test of the serialized JSON content of a metric."""
        name = 'T1'
        description = 'Test'
        operator_str = '=='
        reference_doc = 'TEST-1'
        reference_page = 1
        reference_url = 'example.com'
        params = {'p': Datum(5., 'mag')}
        m = Metric(name, description, operator_str,
                   reference_doc=reference_doc,
                   reference_url=reference_url,
                   reference_page=reference_page,
                   parameters=params)

        j = m.json
        self.assertEqual(j['name'], name)
        self.assertEqual(j['description'], description)
        self.assertEqual(j['operator_str'], operator_str)
        self.assertEqual(j['reference']['doc'], reference_doc)
        self.assertEqual(j['reference']['page'], reference_page)
        self.assertEqual(j['reference']['url'], reference_url)
        self.assertEqual(j['parameters']['p']['value'], 5.)
        self.assertEqual(j['parameters']['p']['unit'], 'mag')


if __name__ == "__main__":
    unittest.main()
