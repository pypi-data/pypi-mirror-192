"""
Enumeration of common measurement types (or dimensions), for example "chest" for a person, "inseam" for pants, "gauge" for screws, or "wheel" for bicycles.

https://schema.org/MeasurementTypeEnumeration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MeasurementTypeEnumerationInheritedProperties(TypedDict):
    """Enumeration of common measurement types (or dimensions), for example "chest" for a person, "inseam" for pants, "gauge" for screws, or "wheel" for bicycles.

    References:
        https://schema.org/MeasurementTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
        supersededBy: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): Relates a term (i.e. a property, class or enumeration) to one that supersedes it.
    """

    supersededBy: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    


class MeasurementTypeEnumerationProperties(TypedDict):
    """Enumeration of common measurement types (or dimensions), for example "chest" for a person, "inseam" for pants, "gauge" for screws, or "wheel" for bicycles.

    References:
        https://schema.org/MeasurementTypeEnumeration
    Note:
        Model Depth 4
    Attributes:
    """

    

#MeasurementTypeEnumerationInheritedPropertiesTd = MeasurementTypeEnumerationInheritedProperties()
#MeasurementTypeEnumerationPropertiesTd = MeasurementTypeEnumerationProperties()


class AllProperties(MeasurementTypeEnumerationInheritedProperties , MeasurementTypeEnumerationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MeasurementTypeEnumerationProperties, MeasurementTypeEnumerationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MeasurementTypeEnumeration"
    return model
    

MeasurementTypeEnumeration = create_schema_org_model()