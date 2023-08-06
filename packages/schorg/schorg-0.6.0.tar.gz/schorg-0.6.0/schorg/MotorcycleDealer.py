"""
A motorcycle dealer.

https://schema.org/MotorcycleDealer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class MotorcycleDealerInheritedProperties(TypedDict):
    """A motorcycle dealer.

    References:
        https://schema.org/MotorcycleDealer
    Note:
        Model Depth 5
    Attributes:
    """

    


class MotorcycleDealerProperties(TypedDict):
    """A motorcycle dealer.

    References:
        https://schema.org/MotorcycleDealer
    Note:
        Model Depth 5
    Attributes:
    """

    

#MotorcycleDealerInheritedPropertiesTd = MotorcycleDealerInheritedProperties()
#MotorcycleDealerPropertiesTd = MotorcycleDealerProperties()


class AllProperties(MotorcycleDealerInheritedProperties , MotorcycleDealerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[MotorcycleDealerProperties, MotorcycleDealerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "MotorcycleDealer"
    return model
    

MotorcycleDealer = create_schema_org_model()