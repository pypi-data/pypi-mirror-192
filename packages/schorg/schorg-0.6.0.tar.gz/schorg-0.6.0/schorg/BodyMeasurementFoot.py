"""
Foot length (measured between end of the most prominent toe and the most prominent part of the heel). Used, for example, to measure socks.

https://schema.org/BodyMeasurementFoot
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementFootInheritedProperties(TypedDict):
    """Foot length (measured between end of the most prominent toe and the most prominent part of the heel). Used, for example, to measure socks.

    References:
        https://schema.org/BodyMeasurementFoot
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementFootProperties(TypedDict):
    """Foot length (measured between end of the most prominent toe and the most prominent part of the heel). Used, for example, to measure socks.

    References:
        https://schema.org/BodyMeasurementFoot
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementFootInheritedPropertiesTd = BodyMeasurementFootInheritedProperties()
#BodyMeasurementFootPropertiesTd = BodyMeasurementFootProperties()


class AllProperties(BodyMeasurementFootInheritedProperties , BodyMeasurementFootProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementFootProperties, BodyMeasurementFootInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementFoot"
    return model
    

BodyMeasurementFoot = create_schema_org_model()