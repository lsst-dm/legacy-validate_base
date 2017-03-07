#!/usr/bin/env python
# See COPYRIGHT file at the top of the source tree.
from __future__ import print_function, division

import unittest

import astropy.units as u

from lsst.validate.base import Specification


class SpecificationTestCase(unittest.TestCase):
    """Test Specification class functionality."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_quantity(self):
        """Test creating and accessing a specification from a quantity."""
        s = Specification('design', 5 * u.mag)
        self.assertEqual(s.quantity.value, 5.)
        self.assertEqual(s.unit, u.mag)
        self.assertEqual(s.unit_str, 'mag')

        # test json output
        json_data = s.json
        self.assertEqual(json_data['name'], 'design')
        self.assertEqual(json_data['value'], 5.)
        self.assertEqual(json_data['unit'], 'mag')

        # rebuild from json
        s2 = Specification.from_json(json_data)
        self.assertEqual(s.name, s2.name)
        self.assertEqual(s.quantity, s2.quantity)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 5. * u.mag)
        self.assertEqual(d.label, 'design')

    def test_unitless(self):
        """Test unitless specifications."""
        s = Specification('design', 100. * u.dimensionless_unscaled)
        self.assertEqual(s.quantity.value, 100.)
        self.assertEqual(s.unit, u.dimensionless_unscaled)
        self.assertEqual(s.unit_str, '')

        # test json output
        json_data = s.json
        self.assertEqual(json_data['name'], 'design')
        self.assertEqual(json_data['value'], 100.)
        self.assertEqual(json_data['unit'], '')

        # rebuild from json
        s2 = Specification.from_json(json_data)
        self.assertEqual(s.name, s2.name)
        self.assertEqual(s.quantity, s2.quantity)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 100. * u.dimensionless_unscaled)
        self.assertEqual(d.label, 'design')


if __name__ == "__main__":
    unittest.main()
