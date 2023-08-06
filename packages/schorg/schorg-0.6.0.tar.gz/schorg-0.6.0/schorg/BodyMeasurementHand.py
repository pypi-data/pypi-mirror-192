"""
Maximum hand girth (measured over the knuckles of the open right hand excluding thumb, fingers together). Used, for example, to fit gloves.

https://schema.org/BodyMeasurementHand
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementHandInheritedProperties(TypedDict):
    """Maximum hand girth (measured over the knuckles of the open right hand excluding thumb, fingers together). Used, for example, to fit gloves.

    References:
        https://schema.org/BodyMeasurementHand
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementHandProperties(TypedDict):
    """Maximum hand girth (measured over the knuckles of the open right hand excluding thumb, fingers together). Used, for example, to fit gloves.

    References:
        https://schema.org/BodyMeasurementHand
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementHandInheritedPropertiesTd = BodyMeasurementHandInheritedProperties()
#BodyMeasurementHandPropertiesTd = BodyMeasurementHandProperties()


class AllProperties(BodyMeasurementHandInheritedProperties , BodyMeasurementHandProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementHandProperties, BodyMeasurementHandInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementHand"
    return model
    

BodyMeasurementHand = create_schema_org_model()