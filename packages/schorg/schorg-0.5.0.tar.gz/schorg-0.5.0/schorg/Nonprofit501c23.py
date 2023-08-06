"""
Nonprofit501c23: Non-profit type referring to Veterans Organizations.

https://schema.org/Nonprofit501c23
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c23InheritedProperties(TypedDict):
    """Nonprofit501c23: Non-profit type referring to Veterans Organizations.

    References:
        https://schema.org/Nonprofit501c23
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c23Properties(TypedDict):
    """Nonprofit501c23: Non-profit type referring to Veterans Organizations.

    References:
        https://schema.org/Nonprofit501c23
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c23InheritedPropertiesTd = Nonprofit501c23InheritedProperties()
#Nonprofit501c23PropertiesTd = Nonprofit501c23Properties()


class AllProperties(Nonprofit501c23InheritedProperties , Nonprofit501c23Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c23Properties, Nonprofit501c23InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c23"
    return model
    

Nonprofit501c23 = create_schema_org_model()