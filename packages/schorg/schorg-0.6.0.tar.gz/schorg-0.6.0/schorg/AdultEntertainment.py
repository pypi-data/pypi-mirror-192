"""
An adult entertainment establishment.

https://schema.org/AdultEntertainment
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AdultEntertainmentInheritedProperties(TypedDict):
    """An adult entertainment establishment.

    References:
        https://schema.org/AdultEntertainment
    Note:
        Model Depth 5
    Attributes:
    """

    


class AdultEntertainmentProperties(TypedDict):
    """An adult entertainment establishment.

    References:
        https://schema.org/AdultEntertainment
    Note:
        Model Depth 5
    Attributes:
    """

    

#AdultEntertainmentInheritedPropertiesTd = AdultEntertainmentInheritedProperties()
#AdultEntertainmentPropertiesTd = AdultEntertainmentProperties()


class AllProperties(AdultEntertainmentInheritedProperties , AdultEntertainmentProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AdultEntertainmentProperties, AdultEntertainmentInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AdultEntertainment"
    return model
    

AdultEntertainment = create_schema_org_model()