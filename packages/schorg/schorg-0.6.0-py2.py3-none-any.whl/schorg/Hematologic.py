"""
A specific branch of medical science that pertains to diagnosis and treatment of disorders of blood and blood producing organs.

https://schema.org/Hematologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class HematologicInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of blood and blood producing organs.

    References:
        https://schema.org/Hematologic
    Note:
        Model Depth 6
    Attributes:
    """

    


class HematologicProperties(TypedDict):
    """A specific branch of medical science that pertains to diagnosis and treatment of disorders of blood and blood producing organs.

    References:
        https://schema.org/Hematologic
    Note:
        Model Depth 6
    Attributes:
    """

    

#HematologicInheritedPropertiesTd = HematologicInheritedProperties()
#HematologicPropertiesTd = HematologicProperties()


class AllProperties(HematologicInheritedProperties , HematologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[HematologicProperties, HematologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Hematologic"
    return model
    

Hematologic = create_schema_org_model()