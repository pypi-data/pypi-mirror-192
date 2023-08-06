"""
A post office.

https://schema.org/PostOffice
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class PostOfficeInheritedProperties(TypedDict):
    """A post office.

    References:
        https://schema.org/PostOffice
    Note:
        Model Depth 5
    Attributes:
    """

    


class PostOfficeProperties(TypedDict):
    """A post office.

    References:
        https://schema.org/PostOffice
    Note:
        Model Depth 5
    Attributes:
    """

    

#PostOfficeInheritedPropertiesTd = PostOfficeInheritedProperties()
#PostOfficePropertiesTd = PostOfficeProperties()


class AllProperties(PostOfficeInheritedProperties , PostOfficeProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[PostOfficeProperties, PostOfficeInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "PostOffice"
    return model
    

PostOffice = create_schema_org_model()