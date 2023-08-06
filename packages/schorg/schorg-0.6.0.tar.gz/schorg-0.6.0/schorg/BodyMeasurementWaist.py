"""
Girth of natural waistline (between hip bones and lower ribs). Used, for example, to fit pants.

https://schema.org/BodyMeasurementWaist
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementWaistInheritedProperties(TypedDict):
    """Girth of natural waistline (between hip bones and lower ribs). Used, for example, to fit pants.

    References:
        https://schema.org/BodyMeasurementWaist
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementWaistProperties(TypedDict):
    """Girth of natural waistline (between hip bones and lower ribs). Used, for example, to fit pants.

    References:
        https://schema.org/BodyMeasurementWaist
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementWaistInheritedPropertiesTd = BodyMeasurementWaistInheritedProperties()
#BodyMeasurementWaistPropertiesTd = BodyMeasurementWaistProperties()


class AllProperties(BodyMeasurementWaistInheritedProperties , BodyMeasurementWaistProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementWaistProperties, BodyMeasurementWaistInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementWaist"
    return model
    

BodyMeasurementWaist = create_schema_org_model()