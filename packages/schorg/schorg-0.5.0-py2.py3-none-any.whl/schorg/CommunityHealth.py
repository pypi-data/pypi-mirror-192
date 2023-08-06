"""
A field of public health focusing on improving health characteristics of a defined population in relation with their geographical or environment areas.

https://schema.org/CommunityHealth
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class CommunityHealthInheritedProperties(TypedDict):
    """A field of public health focusing on improving health characteristics of a defined population in relation with their geographical or environment areas.

    References:
        https://schema.org/CommunityHealth
    Note:
        Model Depth 5
    Attributes:
    """

    


class CommunityHealthProperties(TypedDict):
    """A field of public health focusing on improving health characteristics of a defined population in relation with their geographical or environment areas.

    References:
        https://schema.org/CommunityHealth
    Note:
        Model Depth 5
    Attributes:
    """

    

#CommunityHealthInheritedPropertiesTd = CommunityHealthInheritedProperties()
#CommunityHealthPropertiesTd = CommunityHealthProperties()


class AllProperties(CommunityHealthInheritedProperties , CommunityHealthProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[CommunityHealthProperties, CommunityHealthInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "CommunityHealth"
    return model
    

CommunityHealth = create_schema_org_model()