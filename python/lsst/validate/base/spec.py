# See COPYRIGHT file at the top of the source tree.
from __future__ import print_function, division

import operator

from .jsonmixin import JsonSerializationMixin
from .datum import Datum


__all__ = ['ThresholdSpecification']


class ThresholdSpecification(JsonSerializationMixin):
    """A threshold-type specification, associated with a `Metric`, that
    defines a binary comparison against a measurement.

    Parameters
    ----------
    name : `str`
        Name of the specification for a metric. LPM-17, for example,
        uses ``'design'``, ``'minimum'`` and ``'stretch'`` terminology.
    quantity : `astropy.units.Quantity`
        The specification threshold level.
    """

    name = None
    """Name of the specification for a metric.

    LPM-17, for example, uses ``'design'``, ``'minimum'`` and ``'stretch'``
    terminology.
    """

    threshold = None
    """The specification threshold level (`astropy.units.Quantity`)."""

    def __init__(self, name, threshold, operator_str):
        self.name = name
        self.threshold = threshold
        self.operator_str = operator_str

    @property
    def type(self):
        return 'threshold'

    @property
    def datum(self):
        """Representation of this `Specification`\ 's threshold as a `Datum`.
        """
        return Datum(self.threshold, label=self.name)

    @classmethod
    def from_yaml_doc(cls, yaml_doc):
        """Create a `Specification` from a YAML document, inheriting from
        referenced specifications and partials in a `SpecificationSet`.

        **TODO:** add ``spec_set`` as an attribute so that specifications
        can be inherited.

        Parameters
        ----------
        yaml_doc : `dict`
            Parsed YAML document for a single specification.
        spec_set : `SpecificationSet`
            SpecificationSet that may be used to resolve inheritance in a
            ``yaml_doc``.

        Returns
        -------
        spec : `Specification`
            A `Specification` instance.
        """
        q = Datum._rebuild_quantity(
            yaml_doc['threshold']['value'],
            yaml_doc['threshold']['unit'])
        return cls(yaml_doc['name'], q, yaml_doc['threshold']['operator'])

    @classmethod
    def from_json(cls, json_data):
        """Construct a `ThresholdSpecification` from a JSON document.

        Parameters
        ----------
        json_data : `dict`
            ThresholdSpecification JSON object.

        Returns
        -------
        specification : `Specification`
            Specification from JSON.
        """
        q = Datum._rebuild_quantity(
            json_data['threshold']['value'],
            json_data['threshold']['unit'])
        s = cls(name=json_data['name'],
                threshold=q,
                operator_str=json_data['threshold']['operator'])
        return s

    @property
    def json(self):
        """`dict` that can be serialized as semantic JSON, compatible with
        the SQUASH metric service.
        """
        return JsonSerializationMixin.jsonify_dict({
            'name': self.name,
            'type': self.type,
            'threshold': {
                'value': self.threshold.value,
                'unit': self.threshold.unit.to_string(),
                'operator': self.operator_str
            }})

    @property
    def operator_str(self):
        """Threshold comparision operator ('str').

        A measurement *passes* the specification if::

           measurement {{ operator }} threshold == True

        The operator string is a standard Python binary comparison token, such
        as: ``'<'``, ``'>'``, ``'<='``, ``'>='``, ``'=='`` or ``'!='``.
        """
        return self._operator_str

    @operator_str.setter
    def operator_str(self, v):
        # Cache the operator function as a means of validating the input too
        self._operator = ThresholdSpecification.convert_operator_str(v)
        self._operator_str = v

    @property
    def operator(self):
        """Binary comparision operator that tests success of a measurement
        fulfilling a specification of this metric.

        Measured value is on left side of comparison and specification level
        is on right side.
        """
        return self._operator

    @staticmethod
    def convert_operator_str(op_str):
        """Convert a string representing a binary comparison operator to
        the operator function itself.

        Operators are oriented so that the measurement is on the left-hand
        side, and specification threshold on the right hand side.

        The following operators are permitted:

        ========== =============
        ``op_str`` Function
        ========== =============
        ``>=``     `operator.ge`
        ``>``      `operator.gt`
        ``<``      `operator.lt`
        ``<=``     `operator.le`
        ``==``     `operator.eq`
        ``!=``     `operator.ne`
        ========== =============

        Parameters
        ----------
        op_str : `str`
            A string representing a binary operator.

        Returns
        -------
        op_func : obj
            An operator function from the `operator` standard library
            module.
        """
        operators = {'>=': operator.ge,
                     '>': operator.gt,
                     '<': operator.lt,
                     '<=': operator.le,
                     '==': operator.eq,
                     '!=': operator.ne}
        return operators[op_str]

    def check(self, measurement):
        """Check if a measurement passes this specification.

        Parameters
        ----------
        measurement : `astropy.units.Quantity`
            The measurement value. The measurement `~astropy.units.Quantity`
            must have units *compatible* with `threshold`.

        Returns
        -------
        passed : `bool`
            `True` if the measurement meets the specification,
            `False` otherwise.
        """
        return self.operator(measurement, self.threshold)
