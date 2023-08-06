"""
Nonprofit501k: Non-profit type referring to Child Care Organizations.

https://schema.org/Nonprofit501k
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501kInheritedProperties(TypedDict):
    """Nonprofit501k: Non-profit type referring to Child Care Organizations.

    References:
        https://schema.org/Nonprofit501k
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501kProperties(TypedDict):
    """Nonprofit501k: Non-profit type referring to Child Care Organizations.

    References:
        https://schema.org/Nonprofit501k
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501kInheritedPropertiesTd = Nonprofit501kInheritedProperties()
#Nonprofit501kPropertiesTd = Nonprofit501kProperties()


class AllProperties(Nonprofit501kInheritedProperties , Nonprofit501kProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501kProperties, Nonprofit501kInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501k"
    return model
    

Nonprofit501k = create_schema_org_model()