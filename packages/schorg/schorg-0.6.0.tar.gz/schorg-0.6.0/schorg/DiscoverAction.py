"""
The act of discovering/finding an object.

https://schema.org/DiscoverAction
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class DiscoverActionInheritedProperties(TypedDict):
    """The act of discovering/finding an object.

    References:
        https://schema.org/DiscoverAction
    Note:
        Model Depth 4
    Attributes:
    """

    


class DiscoverActionProperties(TypedDict):
    """The act of discovering/finding an object.

    References:
        https://schema.org/DiscoverAction
    Note:
        Model Depth 4
    Attributes:
    """

    

#DiscoverActionInheritedPropertiesTd = DiscoverActionInheritedProperties()
#DiscoverActionPropertiesTd = DiscoverActionProperties()


class AllProperties(DiscoverActionInheritedProperties , DiscoverActionProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[DiscoverActionProperties, DiscoverActionInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "DiscoverAction"
    return model
    

DiscoverAction = create_schema_org_model()