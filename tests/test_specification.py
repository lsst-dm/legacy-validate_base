#!/usr/bin/env python
# See COPYRIGHT file at the top of the source tree.

import unittest

import astropy.units as u

from lsst.validate.base import Specification, Datum


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
        self.assertEqual(s.filter_names, s2.filter_names)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 5. * u.mag)
        self.assertEqual(d.label, 'design')

    def test_from_value(self):
        """Test creating a specification from a value."""
        s = Specification('design', 5., unit='mag')
        self.assertEqual(s.quantity.value, 5.)
        self.assertEqual(s.unit, u.mag)
        self.assertEqual(s.unit_str, 'mag')
        self.assertEqual(s.name, 'design')

        # test json output
        json_data = s.json
        self.assertEqual(json_data['name'], 'design')
        self.assertEqual(json_data['value'], 5.)
        self.assertEqual(json_data['unit'], 'mag')

        # rebuild from json
        s2 = Specification.from_json(json_data)
        self.assertEqual(s.name, s2.name)
        self.assertEqual(s.quantity, s2.quantity)
        self.assertEqual(s.filter_names, s2.filter_names)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 5. * u.mag)
        self.assertEqual(d.label, 'design')

    def test_unitless(self):
        """Test unitless specifications."""
        s = Specification('design', 100., unit='')
        self.assertEqual(s.quantity.value, 100.)
        self.assertEqual(s.unit, u.Unit(''))
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
        self.assertEqual(s.filter_names, s2.filter_names)

        # test datum output
        d = s.datum
        self.assertEqual(d.quantity, 100. * u.Unit(''))
        self.assertEqual(d.label, 'design')

    def test_unitless_int(self):
        """Test that a specification can be a unitless integer (count)."""
        s = Specification('design', 10)
        self.assertEqual(s.quantity, 10)

        # test JSON output
        json_data = s.json
        self.assertEqual(json_data['value'], 10)

        # rebuild from JSON
        s2 = Specification.from_json(json_data)
        self.assertEqual(s.quantity, s2.quantity)

    def test_filters(self):
        """Test setting filter dependencies."""
        filter_names = ['u', 'g']
        s = Specification('design', 5 * u.mag, filter_names=filter_names)
        for filter_name in s.filter_names:
            self.assertIn(filter_name, filter_names)
        self.assertEqual(len(filter_names), len(s.filter_names))

    def test_dependency_access(self):
        deps = {'a': Datum(5., 'mag')}
        s = Specification('design', 0., '', dependencies=deps)
        self.assertEqual(s.a.quantity, 5. * u.mag)
        json_data = s.json
        self.assertEqual(json_data['dependencies']['a']['value'], 5.)
        self.assertEqual(json_data['dependencies']['a']['unit'], 'mag')


if __name__ == "__main__":
    unittest.main()
