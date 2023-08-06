"""
An car dealership.

https://schema.org/AutoDealer
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class AutoDealerInheritedProperties(TypedDict):
    """An car dealership.

    References:
        https://schema.org/AutoDealer
    Note:
        Model Depth 5
    Attributes:
    """

    


class AutoDealerProperties(TypedDict):
    """An car dealership.

    References:
        https://schema.org/AutoDealer
    Note:
        Model Depth 5
    Attributes:
    """

    

#AutoDealerInheritedPropertiesTd = AutoDealerInheritedProperties()
#AutoDealerPropertiesTd = AutoDealerProperties()


class AllProperties(AutoDealerInheritedProperties , AutoDealerProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[AutoDealerProperties, AutoDealerInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "AutoDealer"
    return model
    

AutoDealer = create_schema_org_model()