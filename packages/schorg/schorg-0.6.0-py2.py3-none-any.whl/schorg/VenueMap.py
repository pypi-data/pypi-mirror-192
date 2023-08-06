"""
A venue map (e.g. for malls, auditoriums, museums, etc.).

https://schema.org/VenueMap
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class VenueMapInheritedProperties(TypedDict):
    """A venue map (e.g. for malls, auditoriums, museums, etc.).

    References:
        https://schema.org/VenueMap
    Note:
        Model Depth 5
    Attributes:
    """

    


class VenueMapProperties(TypedDict):
    """A venue map (e.g. for malls, auditoriums, museums, etc.).

    References:
        https://schema.org/VenueMap
    Note:
        Model Depth 5
    Attributes:
    """

    

#VenueMapInheritedPropertiesTd = VenueMapInheritedProperties()
#VenueMapPropertiesTd = VenueMapProperties()


class AllProperties(VenueMapInheritedProperties , VenueMapProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[VenueMapProperties, VenueMapInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "VenueMap"
    return model
    

VenueMap = create_schema_org_model()