"""
A structured value providing information about when a certain organization or person owned a certain product.

https://schema.org/OwnershipInfo
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class OwnershipInfoInheritedProperties(TypedDict):
    """A structured value providing information about when a certain organization or person owned a certain product.

    References:
        https://schema.org/OwnershipInfo
    Note:
        Model Depth 4
    Attributes:
    """

    


class OwnershipInfoProperties(TypedDict):
    """A structured value providing information about when a certain organization or person owned a certain product.

    References:
        https://schema.org/OwnershipInfo
    Note:
        Model Depth 4
    Attributes:
        ownedThrough: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The date and time of giving up ownership on the product.
        ownedFrom: (Optional[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]): The date and time of obtaining the product.
        acquiredFrom: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The organization or person from which the product was acquired.
        typeOfGood: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The product that this structured value is referring to.
    """

    ownedThrough: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    ownedFrom: NotRequired[Union[List[Union[datetime, SchemaOrgObj, str]], datetime, SchemaOrgObj, str]]
    acquiredFrom: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    typeOfGood: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#OwnershipInfoInheritedPropertiesTd = OwnershipInfoInheritedProperties()
#OwnershipInfoPropertiesTd = OwnershipInfoProperties()


class AllProperties(OwnershipInfoInheritedProperties , OwnershipInfoProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[OwnershipInfoProperties, OwnershipInfoInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "OwnershipInfo"
    return model
    

OwnershipInfo = create_schema_org_model()