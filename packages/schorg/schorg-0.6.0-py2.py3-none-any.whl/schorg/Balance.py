"""
Physical activity that is engaged to help maintain posture and balance.

https://schema.org/Balance
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class BalanceInheritedProperties(TypedDict):
    """Physical activity that is engaged to help maintain posture and balance.

    References:
        https://schema.org/Balance
    Note:
        Model Depth 5
    Attributes:
    """

    


class BalanceProperties(TypedDict):
    """Physical activity that is engaged to help maintain posture and balance.

    References:
        https://schema.org/Balance
    Note:
        Model Depth 5
    Attributes:
    """

    

#BalanceInheritedPropertiesTd = BalanceInheritedProperties()
#BalancePropertiesTd = BalanceProperties()


class AllProperties(BalanceInheritedProperties , BalanceProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[BalanceProperties, BalanceInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "Balance"
    return model
    

Balance = create_schema_org_model()