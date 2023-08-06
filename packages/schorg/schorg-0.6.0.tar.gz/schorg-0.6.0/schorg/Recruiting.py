"""
Recruiting participants.

https://schema.org/Recruiting
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class RecruitingInheritedProperties(TypedDict):
    """Recruiting participants.

    References:
        https://schema.org/Recruiting
    Note:
        Model Depth 6
    Attributes:
    """

    


class RecruitingProperties(TypedDict):
    """Recruiting participants.

    References:
        https://schema.org/Recruiting
    Note:
        Model Depth 6
    Attributes:
    """

    

#RecruitingInheritedPropertiesTd = RecruitingInheritedProperties()
#RecruitingPropertiesTd = RecruitingProperties()


class AllProperties(RecruitingInheritedProperties , RecruitingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[RecruitingProperties, RecruitingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Recruiting"
    return model
    

Recruiting = create_schema_org_model()