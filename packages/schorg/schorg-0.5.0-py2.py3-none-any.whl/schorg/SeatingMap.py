"""
A seating map.

https://schema.org/SeatingMap
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SeatingMapInheritedProperties(TypedDict):
    """A seating map.

    References:
        https://schema.org/SeatingMap
    Note:
        Model Depth 5
    Attributes:
    """

    


class SeatingMapProperties(TypedDict):
    """A seating map.

    References:
        https://schema.org/SeatingMap
    Note:
        Model Depth 5
    Attributes:
    """

    

#SeatingMapInheritedPropertiesTd = SeatingMapInheritedProperties()
#SeatingMapPropertiesTd = SeatingMapProperties()


class AllProperties(SeatingMapInheritedProperties , SeatingMapProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SeatingMapProperties, SeatingMapInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SeatingMap"
    return model
    

SeatingMap = create_schema_org_model()