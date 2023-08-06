"""
Nonprofit501c19: Non-profit type referring to Post or Organization of Past or Present Members of the Armed Forces.

https://schema.org/Nonprofit501c19
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class Nonprofit501c19InheritedProperties(TypedDict):
    """Nonprofit501c19: Non-profit type referring to Post or Organization of Past or Present Members of the Armed Forces.

    References:
        https://schema.org/Nonprofit501c19
    Note:
        Model Depth 6
    Attributes:
    """

    


class Nonprofit501c19Properties(TypedDict):
    """Nonprofit501c19: Non-profit type referring to Post or Organization of Past or Present Members of the Armed Forces.

    References:
        https://schema.org/Nonprofit501c19
    Note:
        Model Depth 6
    Attributes:
    """

    

#Nonprofit501c19InheritedPropertiesTd = Nonprofit501c19InheritedProperties()
#Nonprofit501c19PropertiesTd = Nonprofit501c19Properties()


class AllProperties(Nonprofit501c19InheritedProperties , Nonprofit501c19Properties, TypedDict):
    pass


def create_schema_org_model(type_: Union[Nonprofit501c19Properties, Nonprofit501c19InheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Nonprofit501c19"
    return model
    

Nonprofit501c19 = create_schema_org_model()