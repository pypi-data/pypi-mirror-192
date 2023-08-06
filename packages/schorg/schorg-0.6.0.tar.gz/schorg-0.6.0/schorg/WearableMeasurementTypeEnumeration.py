"""
Enumerates common types of measurement for wearables products.

https://schema.org/WearableMeasurementTypeEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WearableMeasurementTypeEnumerationInheritedProperties(TypedDict):
    """Enumerates common types of measurement for wearables products.

    References:
        https://schema.org/WearableMeasurementTypeEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    


class WearableMeasurementTypeEnumerationProperties(TypedDict):
    """Enumerates common types of measurement for wearables products.

    References:
        https://schema.org/WearableMeasurementTypeEnumeration
    Note:
        Model Depth 5
    Attributes:
    """

    

#WearableMeasurementTypeEnumerationInheritedPropertiesTd = WearableMeasurementTypeEnumerationInheritedProperties()
#WearableMeasurementTypeEnumerationPropertiesTd = WearableMeasurementTypeEnumerationProperties()


class AllProperties(WearableMeasurementTypeEnumerationInheritedProperties , WearableMeasurementTypeEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WearableMeasurementTypeEnumerationProperties, WearableMeasurementTypeEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WearableMeasurementTypeEnumeration"
    return model
    

WearableMeasurementTypeEnumeration = create_schema_org_model()