"""
Indicates that the item is available only at physical locations.

https://schema.org/InStoreOnly
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class InStoreOnlyInheritedProperties(TypedDict):
    """Indicates that the item is available only at physical locations.

    References:
        https://schema.org/InStoreOnly
    Note:
        Model Depth 5
    Attributes:
    """

    


class InStoreOnlyProperties(TypedDict):
    """Indicates that the item is available only at physical locations.

    References:
        https://schema.org/InStoreOnly
    Note:
        Model Depth 5
    Attributes:
    """

    

#InStoreOnlyInheritedPropertiesTd = InStoreOnlyInheritedProperties()
#InStoreOnlyPropertiesTd = InStoreOnlyProperties()


class AllProperties(InStoreOnlyInheritedProperties , InStoreOnlyProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[InStoreOnlyProperties, InStoreOnlyInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "InStoreOnly"
    return model
    

InStoreOnly = create_schema_org_model()