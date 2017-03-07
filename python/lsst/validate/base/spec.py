# See COPYRIGHT file at the top of the source tree.
from __future__ import print_function, division

import astropy.units as u

from .jsonmixin import JsonSerializationMixin
from .datum import Datum, QuantityAttributeMixin


__all__ = ['Specification']


class Specification(QuantityAttributeMixin, JsonSerializationMixin):
    """A specification level, or threshold, associated with a `Metric`.

    Parameters
    ----------
    name : `str`
        Name of the specification level for a metric. LPM-17, for example,
        uses ``'design'``, ``'minimum'`` and ``'stretch'`` terminology.
    quantity : `astropy.units.Quantity`
        The specification threshold level.
    """

    name = None
    """Name of the specification level for a metric.

    LPM-17, for example, uses ``'design'``, ``'minimum'`` and ``'stretch'``
    terminology.
    """

    quantity = None
    """The specification threshold level (`astropy.units.Quantity`)."""

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    @property
    def datum(self):
        """Representation of this `Specification` as a `Datum`."""
        return Datum(self.quantity, label=self.name)

    @classmethod
    def from_json(cls, json_data):
        """Construct a Specification from a JSON document.

        Parameters
        ----------
        json_data : `dict`
            Specification JSON object.

        Returns
        -------
        specification : `Specification`
            Specification from JSON.
        """
        q = Datum._rebuild_quantity(json_data['value'], json_data['unit'])
        s = cls(name=json_data['name'],
                quantity=q)
        return s

    @property
    def json(self):
        """`dict` that can be serialized as semantic JSON, compatible with
        the SQUASH metric service.
        """
        if isinstance(self.quantity, u.Quantity):
            v = self.quantity.value
        else:
            v = self.quantity
        return JsonSerializationMixin.jsonify_dict({
            'name': self.name,
            'value': v,
            'unit': self.unit_str})
