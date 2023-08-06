"""
A type of blood vessel that specifically carries blood away from the heart.

https://schema.org/Artery
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ArteryInheritedProperties(TypedDict):
    """A type of blood vessel that specifically carries blood away from the heart.

    References:
        https://schema.org/Artery
    Note:
        Model Depth 5
    Attributes:
    """

    


class ArteryProperties(TypedDict):
    """A type of blood vessel that specifically carries blood away from the heart.

    References:
        https://schema.org/Artery
    Note:
        Model Depth 5
    Attributes:
        arterialBranch: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The branches that comprise the arterial structure.
        supplyTo: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The area to which the artery supplies blood.
    """

    arterialBranch: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    supplyTo: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#ArteryInheritedPropertiesTd = ArteryInheritedProperties()
#ArteryPropertiesTd = ArteryProperties()


class AllProperties(ArteryInheritedProperties , ArteryProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ArteryProperties, ArteryInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Artery"
    return model
    

Artery = create_schema_org_model()