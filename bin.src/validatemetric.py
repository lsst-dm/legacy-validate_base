#!/usr/bin/env python
# See COPYRIGHT file at the top of the source tree.
"""Validate the schema of a metric YAML document.
"""
import sys
import os
import argparse

import yaml
from jsonschema.exceptions import ValidationError

from lsst.validate.base import Metric


def main():
    copyright_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'COPYRIGHT'))
    with open(copyright_path) as f:
        copyright = f.read()

    parser = argparse.ArgumentParser(
        description='Validate the schema of a metric.yaml file that defines '
                    'metrics in the lsst.validate.base framework.',
        epilog=copyright)
    parser.add_argument(
        dest='metric_path',
        help='Path of a metric.yaml file to validate')
    args = parser.parse_args()

    with open(args.metric_path) as f:
        yaml_doc = yaml.safe_load(f)

    try:
        Metric.validate_metric_doc(yaml_doc)
    except ValidationError as e:
        print(e)
        print('Invalid schema: {0}'.format(args.metric_path))
        sys.exit(1)

    print('Valid schema: {0}'.format(args.metric_path))
    sys.exit(0)


if __name__ == '__main__':
    main()
