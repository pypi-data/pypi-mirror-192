"""
A specific branch of medical science that pertains to the health care of women, particularly in the diagnosis and treatment of disorders affecting the female reproductive system.

https://schema.org/Gynecologic
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class GynecologicInheritedProperties(TypedDict):
    """A specific branch of medical science that pertains to the health care of women, particularly in the diagnosis and treatment of disorders affecting the female reproductive system.

    References:
        https://schema.org/Gynecologic
    Note:
        Model Depth 5
    Attributes:
    """

    


class GynecologicProperties(TypedDict):
    """A specific branch of medical science that pertains to the health care of women, particularly in the diagnosis and treatment of disorders affecting the female reproductive system.

    References:
        https://schema.org/Gynecologic
    Note:
        Model Depth 5
    Attributes:
    """

    

#GynecologicInheritedPropertiesTd = GynecologicInheritedProperties()
#GynecologicPropertiesTd = GynecologicProperties()


class AllProperties(GynecologicInheritedProperties , GynecologicProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[GynecologicProperties, GynecologicInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Gynecologic"
    return model
    

Gynecologic = create_schema_org_model()