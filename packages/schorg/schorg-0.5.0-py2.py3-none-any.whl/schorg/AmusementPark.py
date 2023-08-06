"""
An amusement park.

https://schema.org/AmusementPark
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AmusementParkInheritedProperties(TypedDict):
    """An amusement park.

    References:
        https://schema.org/AmusementPark
    Note:
        Model Depth 5
    Attributes:
    """

    


class AmusementParkProperties(TypedDict):
    """An amusement park.

    References:
        https://schema.org/AmusementPark
    Note:
        Model Depth 5
    Attributes:
    """

    

#AmusementParkInheritedPropertiesTd = AmusementParkInheritedProperties()
#AmusementParkPropertiesTd = AmusementParkProperties()


class AllProperties(AmusementParkInheritedProperties , AmusementParkProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AmusementParkProperties, AmusementParkInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AmusementPark"
    return model
    

AmusementPark = create_schema_org_model()