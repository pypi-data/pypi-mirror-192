"""
Girth of hips (measured around the buttocks). Used, for example, to fit skirts.

https://schema.org/BodyMeasurementHips
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementHipsInheritedProperties(TypedDict):
    """Girth of hips (measured around the buttocks). Used, for example, to fit skirts.

    References:
        https://schema.org/BodyMeasurementHips
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementHipsProperties(TypedDict):
    """Girth of hips (measured around the buttocks). Used, for example, to fit skirts.

    References:
        https://schema.org/BodyMeasurementHips
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementHipsInheritedPropertiesTd = BodyMeasurementHipsInheritedProperties()
#BodyMeasurementHipsPropertiesTd = BodyMeasurementHipsProperties()


class AllProperties(BodyMeasurementHipsInheritedProperties , BodyMeasurementHipsProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementHipsProperties, BodyMeasurementHipsInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementHips"
    return model
    

BodyMeasurementHips = create_schema_org_model()