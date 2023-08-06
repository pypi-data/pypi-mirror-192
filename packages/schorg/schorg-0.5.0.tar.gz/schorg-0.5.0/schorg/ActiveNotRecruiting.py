"""
Active, but not recruiting new participants.

https://schema.org/ActiveNotRecruiting
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ActiveNotRecruitingInheritedProperties(TypedDict):
    """Active, but not recruiting new participants.

    References:
        https://schema.org/ActiveNotRecruiting
    Note:
        Model Depth 6
    Attributes:
    """

    


class ActiveNotRecruitingProperties(TypedDict):
    """Active, but not recruiting new participants.

    References:
        https://schema.org/ActiveNotRecruiting
    Note:
        Model Depth 6
    Attributes:
    """

    

#ActiveNotRecruitingInheritedPropertiesTd = ActiveNotRecruitingInheritedProperties()
#ActiveNotRecruitingPropertiesTd = ActiveNotRecruitingProperties()


class AllProperties(ActiveNotRecruitingInheritedProperties , ActiveNotRecruitingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ActiveNotRecruitingProperties, ActiveNotRecruitingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ActiveNotRecruiting"
    return model
    

ActiveNotRecruiting = create_schema_org_model()