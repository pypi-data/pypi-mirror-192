"""
A transit map.

https://schema.org/TransitMap
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TransitMapInheritedProperties(TypedDict):
    """A transit map.

    References:
        https://schema.org/TransitMap
    Note:
        Model Depth 5
    Attributes:
    """

    


class TransitMapProperties(TypedDict):
    """A transit map.

    References:
        https://schema.org/TransitMap
    Note:
        Model Depth 5
    Attributes:
    """

    

#TransitMapInheritedPropertiesTd = TransitMapInheritedProperties()
#TransitMapPropertiesTd = TransitMapProperties()


class AllProperties(TransitMapInheritedProperties , TransitMapProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TransitMapProperties, TransitMapInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TransitMap"
    return model
    

TransitMap = create_schema_org_model()