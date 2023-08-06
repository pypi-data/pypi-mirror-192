"""
Not yet recruiting.

https://schema.org/NotYetRecruiting
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class NotYetRecruitingInheritedProperties(TypedDict):
    """Not yet recruiting.

    References:
        https://schema.org/NotYetRecruiting
    Note:
        Model Depth 6
    Attributes:
    """

    


class NotYetRecruitingProperties(TypedDict):
    """Not yet recruiting.

    References:
        https://schema.org/NotYetRecruiting
    Note:
        Model Depth 6
    Attributes:
    """

    

#NotYetRecruitingInheritedPropertiesTd = NotYetRecruitingInheritedProperties()
#NotYetRecruitingPropertiesTd = NotYetRecruitingProperties()


class AllProperties(NotYetRecruitingInheritedProperties , NotYetRecruitingProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[NotYetRecruitingProperties, NotYetRecruitingInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "NotYetRecruiting"
    return model
    

NotYetRecruiting = create_schema_org_model()