"""
A car rental business.

https://schema.org/AutoRental
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutoRentalInheritedProperties(TypedDict):
    """A car rental business.

    References:
        https://schema.org/AutoRental
    Note:
        Model Depth 5
    Attributes:
    """

    


class AutoRentalProperties(TypedDict):
    """A car rental business.

    References:
        https://schema.org/AutoRental
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutoRentalInheritedPropertiesTd = AutoRentalInheritedProperties()
#AutoRentalPropertiesTd = AutoRentalProperties()


class AllProperties(AutoRentalInheritedProperties , AutoRentalProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutoRentalProperties, AutoRentalInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutoRental"
    return model
    

AutoRental = create_schema_org_model()