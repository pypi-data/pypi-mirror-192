"""
Inside leg (measured between crotch and soles of feet). Used, for example, to fit pants.

https://schema.org/BodyMeasurementInsideLeg
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementInsideLegInheritedProperties(TypedDict):
    """Inside leg (measured between crotch and soles of feet). Used, for example, to fit pants.

    References:
        https://schema.org/BodyMeasurementInsideLeg
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementInsideLegProperties(TypedDict):
    """Inside leg (measured between crotch and soles of feet). Used, for example, to fit pants.

    References:
        https://schema.org/BodyMeasurementInsideLeg
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementInsideLegInheritedPropertiesTd = BodyMeasurementInsideLegInheritedProperties()
#BodyMeasurementInsideLegPropertiesTd = BodyMeasurementInsideLegProperties()


class AllProperties(BodyMeasurementInsideLegInheritedProperties , BodyMeasurementInsideLegProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementInsideLegProperties, BodyMeasurementInsideLegInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementInsideLeg"
    return model
    

BodyMeasurementInsideLeg = create_schema_org_model()