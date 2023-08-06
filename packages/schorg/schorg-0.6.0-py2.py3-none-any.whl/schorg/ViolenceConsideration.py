"""
Item shows or promotes violence.

https://schema.org/ViolenceConsideration
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ViolenceConsiderationInheritedProperties(TypedDict):
    """Item shows or promotes violence.

    References:
        https://schema.org/ViolenceConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    


class ViolenceConsiderationProperties(TypedDict):
    """Item shows or promotes violence.

    References:
        https://schema.org/ViolenceConsideration
    Note:
        Model Depth 5
    Attributes:
    """

    

#ViolenceConsiderationInheritedPropertiesTd = ViolenceConsiderationInheritedProperties()
#ViolenceConsiderationPropertiesTd = ViolenceConsiderationProperties()


class AllProperties(ViolenceConsiderationInheritedProperties , ViolenceConsiderationProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ViolenceConsiderationProperties, ViolenceConsiderationInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ViolenceConsideration"
    return model
    

ViolenceConsideration = create_schema_org_model()