"""
Maximum girth of chest. Used, for example, to fit men's suits.

https://schema.org/BodyMeasurementChest
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BodyMeasurementChestInheritedProperties(TypedDict):
    """Maximum girth of chest. Used, for example, to fit men's suits.

    References:
        https://schema.org/BodyMeasurementChest
    Note:
        Model Depth 6
    Attributes:
    """

    


class BodyMeasurementChestProperties(TypedDict):
    """Maximum girth of chest. Used, for example, to fit men's suits.

    References:
        https://schema.org/BodyMeasurementChest
    Note:
        Model Depth 6
    Attributes:
    """

    

#BodyMeasurementChestInheritedPropertiesTd = BodyMeasurementChestInheritedProperties()
#BodyMeasurementChestPropertiesTd = BodyMeasurementChestProperties()


class AllProperties(BodyMeasurementChestInheritedProperties , BodyMeasurementChestProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BodyMeasurementChestProperties, BodyMeasurementChestInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "BodyMeasurementChest"
    return model
    

BodyMeasurementChest = create_schema_org_model()