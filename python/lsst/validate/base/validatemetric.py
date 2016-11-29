# See COPYRIGHT file at the top of the source tree.
import sys
import os
import argparse

import yaml
from jsonschema.exceptions import ValidationError

from lsst.validate.base import Metric


__all__ = ['main', 'parse_args']


def main():
    """Command line entrypoint for validatemetric.py."""
    args = parse_args()

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


def parse_args():
    """Parse validatemetric.py's arguments with `argparse`."""
    copyright_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),
                     '..', '..', '..', '..', 'COPYRIGHT'))
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

    return args
