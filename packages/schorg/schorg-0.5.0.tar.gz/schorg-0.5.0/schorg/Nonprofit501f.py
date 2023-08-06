"""
Nonprofit501f: Non-profit type referring to Cooperative Service Organizations.

https://schema.org/Nonprofit501f
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501fInheritedProperties(TypedDict):
    """Nonprofit501f: Non-profit type referring to Cooperative Service Organizations.

    References:
        https://schema.org/Nonprofit501f
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501fProperties(TypedDict):
    """Nonprofit501f: Non-profit type referring to Cooperative Service Organizations.

    References:
        https://schema.org/Nonprofit501f
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501fInheritedPropertiesTd = Nonprofit501fInheritedProperties()
#Nonprofit501fPropertiesTd = Nonprofit501fProperties()


class AllProperties(Nonprofit501fInheritedProperties , Nonprofit501fProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501fProperties, Nonprofit501fInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501f"
    return model
    

Nonprofit501f = create_schema_org_model()