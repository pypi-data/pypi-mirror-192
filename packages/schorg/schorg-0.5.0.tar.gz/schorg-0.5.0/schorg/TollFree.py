"""
The associated telephone number is toll free.

https://schema.org/TollFree
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class TollFreeInheritedProperties(TypedDict):
    """The associated telephone number is toll free.

    References:
        https://schema.org/TollFree
    Note:
        Model Depth 5
    Attributes:
    """

    


class TollFreeProperties(TypedDict):
    """The associated telephone number is toll free.

    References:
        https://schema.org/TollFree
    Note:
        Model Depth 5
    Attributes:
    """

    

#TollFreeInheritedPropertiesTd = TollFreeInheritedProperties()
#TollFreePropertiesTd = TollFreeProperties()


class AllProperties(TollFreeInheritedProperties , TollFreeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[TollFreeProperties, TollFreeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "TollFree"
    return model
    

TollFree = create_schema_org_model()