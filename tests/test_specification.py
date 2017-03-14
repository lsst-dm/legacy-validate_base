#!/usr/bin/env python
# See COPYRIGHT file at the top of the source tree.
from __future__ import print_function, division

import operator
import unittest

import astropy.units as u

from lsst.validate.base import ThresholdSpecification


class SpecificationTestCase(unittest.TestCase):
    """Test Specification class functionality."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_quantity(self):
        """Test creating and accessing a specification from a quantity."""
        s = ThresholdSpecification('design', 5 * u.mag, '<')
        self.assertEqual(s.threshold.value, 5.)
        self.assertEqual(s.threshold.unit, u.mag)
        self.assertEqual(s.threshold.unit.to_string(), 'mag')
        self.assertEqual(s.operator_str, '<')
        self.assertEqual(s.operator, operator.lt)
        # Test the check method and unit equivalencies
        self.assertTrue(s.check(2. * u.mag))
        self.assertTrue(s.check(2000. * u.mmag))
        self.assertFalse(s.check(7. * u.mag))
        self.assertFalse(s.check(7000. * u.mmag))

        # test json output
        json_data = s.json
        self.assertEqual(json_data['name'], 'design')
        self.assertEqual(json_data['threshold']['value'], 5.)
        self.assertEqual(json_data['threshold']['unit'], 'mag')
        self.assertEqual(json_data['threshold']['operator'], '<')

        # rebuild from json
        s2 = ThresholdSpecification.from_json(json_data)
        self.assertEqual(s.name, s2.name)
        self.assertEqual(s.threshold, s2.threshold)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 5. * u.mag)
        self.assertEqual(d.label, 'design')

    def test_unitless(self):
        """Test unitless specifications."""
        s = ThresholdSpecification('design',
                                   100. * u.dimensionless_unscaled, '<')
        self.assertEqual(s.threshold.value, 100.)
        self.assertEqual(s.threshold.unit, u.dimensionless_unscaled)
        self.assertEqual(s.threshold.unit.to_string(), '')
        # Test the check method
        self.assertTrue(s.check(99. * u.dimensionless_unscaled))
        self.assertFalse(s.check(101. * u.dimensionless_unscaled))

        # test json output
        json_data = s.json
        self.assertEqual(json_data['name'], 'design')
        self.assertEqual(json_data['threshold']['value'], 100.)
        self.assertEqual(json_data['threshold']['unit'], '')
        self.assertEqual(json_data['threshold']['operator'], '<')

        # rebuild from json
        s2 = ThresholdSpecification.from_json(json_data)
        self.assertEqual(s.name, s2.name)
        self.assertEqual(s.threshold, s2.threshold)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 100. * u.dimensionless_unscaled)
        self.assertEqual(d.label, 'design')

    def test_operator_conversion(self):
        """Tests for Metric.convert_operator_str."""
        self.assertTrue(
            ThresholdSpecification.convert_operator_str('>=')(7, 7))
        self.assertTrue(
            ThresholdSpecification.convert_operator_str('>')(7, 5))
        self.assertTrue(
            ThresholdSpecification.convert_operator_str('<')(5, 7))
        self.assertTrue(
            ThresholdSpecification.convert_operator_str('<=')(7, 7))
        self.assertTrue(
            ThresholdSpecification.convert_operator_str('==')(7, 7))
        self.assertTrue(
            ThresholdSpecification.convert_operator_str('!=')(7, 5))


if __name__ == "__main__":
    unittest.main()
