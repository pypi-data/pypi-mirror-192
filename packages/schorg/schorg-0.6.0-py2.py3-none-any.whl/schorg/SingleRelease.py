"""
SingleRelease.

https://schema.org/SingleRelease
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class SingleReleaseInheritedProperties(TypedDict):
    """SingleRelease.

    References:
        https://schema.org/SingleRelease
    Note:
        Model Depth 5
    Attributes:
    """

    


class SingleReleaseProperties(TypedDict):
    """SingleRelease.

    References:
        https://schema.org/SingleRelease
    Note:
        Model Depth 5
    Attributes:
    """

    

#SingleReleaseInheritedPropertiesTd = SingleReleaseInheritedProperties()
#SingleReleasePropertiesTd = SingleReleaseProperties()


class AllProperties(SingleReleaseInheritedProperties , SingleReleaseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[SingleReleaseProperties, SingleReleaseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "SingleRelease"
    return model
    

SingleRelease = create_schema_org_model()