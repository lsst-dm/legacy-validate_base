#!/usr/bin/env python
# See COPYRIGHT file at the top of the source tree.
from __future__ import print_function, division

import unittest

from lsst.validate.base.spec import SpecificationSet, ThresholdSpecification


class TestSimpleSpecificationSet(unittest.TestCase):
    """Test a small specification set."""

    def setUp(self):
        self.pa1_design_gri_doc = {
            'name': 'design_gri',
            'metric': 'PA1',
            'threshold': {
                'value': 5.0,
                'unit': 'mmag',
                'operator': '<='
            }
        }
        pa1_design_gri = ThresholdSpecification.from_yaml_doc(
            self.pa1_design_gri_doc)

        self.pa1_stretch_gri_doc = {
            'name': 'stretch_gri',
            'metric': 'PA1',
            'threshold': {
                'value': 3.0,
                'unit': 'mmag',
                'operator': '<='
            }
        }
        pa1_stretch_gri = ThresholdSpecification.from_yaml_doc(
            self.pa1_stretch_gri_doc)

        specifications = {
            pa1_design_gri.name: pa1_design_gri,
        }
        self.spec_set = SpecificationSet('validate_drp', specifications)
        self.spec_set[pa1_stretch_gri.name] = pa1_stretch_gri

    def test_len(self):
        self.assertEqual(len(self.spec_set), 2)

    def test_contains(self):
        self.assertTrue('design_gri' in self.spec_set)
        self.assertTrue('stretch_gri' in self.spec_set)

    def test_getitem(self):
        # FIXME better to test object equality
        self.assertEqual(self.spec_set['design_gri'].name, 'design_gri')
        self.assertEqual(self.spec_set['stretch_gri'].name, 'stretch_gri')


if __name__ == "__main__":
    unittest.main()
