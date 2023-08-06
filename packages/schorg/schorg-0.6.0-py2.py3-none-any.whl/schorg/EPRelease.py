"""
EPRelease.

https://schema.org/EPRelease
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class EPReleaseInheritedProperties(TypedDict):
    """EPRelease.

    References:
        https://schema.org/EPRelease
    Note:
        Model Depth 5
    Attributes:
    """

    


class EPReleaseProperties(TypedDict):
    """EPRelease.

    References:
        https://schema.org/EPRelease
    Note:
        Model Depth 5
    Attributes:
    """

    

#EPReleaseInheritedPropertiesTd = EPReleaseInheritedProperties()
#EPReleasePropertiesTd = EPReleaseProperties()


class AllProperties(EPReleaseInheritedProperties , EPReleaseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[EPReleaseProperties, EPReleaseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "EPRelease"
    return model
    

EPRelease = create_schema_org_model()