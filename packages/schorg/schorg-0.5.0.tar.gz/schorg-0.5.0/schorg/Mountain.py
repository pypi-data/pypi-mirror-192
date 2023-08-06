"""
A mountain, like Mount Whitney or Mount Everest.

https://schema.org/Mountain
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MountainInheritedProperties(TypedDict):
    """A mountain, like Mount Whitney or Mount Everest.

    References:
        https://schema.org/Mountain
    Note:
        Model Depth 4
    Attributes:
    """

    


class MountainProperties(TypedDict):
    """A mountain, like Mount Whitney or Mount Everest.

    References:
        https://schema.org/Mountain
    Note:
        Model Depth 4
    Attributes:
    """

    

#MountainInheritedPropertiesTd = MountainInheritedProperties()
#MountainPropertiesTd = MountainProperties()


class AllProperties(MountainInheritedProperties , MountainProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MountainProperties, MountainInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Mountain"
    return model
    

Mountain = create_schema_org_model()