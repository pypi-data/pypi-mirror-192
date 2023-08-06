"""
A structured value representing the duration and scope of services that will be provided to a customer free of charge in case of a defect or malfunction of a product.

https://schema.org/WarrantyPromise
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class WarrantyPromiseInheritedProperties(TypedDict):
    """A structured value representing the duration and scope of services that will be provided to a customer free of charge in case of a defect or malfunction of a product.

    References:
        https://schema.org/WarrantyPromise
    Note:
        Model Depth 4
    Attributes:
    """

    


class WarrantyPromiseProperties(TypedDict):
    """A structured value representing the duration and scope of services that will be provided to a customer free of charge in case of a defect or malfunction of a product.

    References:
        https://schema.org/WarrantyPromise
    Note:
        Model Depth 4
    Attributes:
        warrantyScope: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The scope of the warranty promise.
        durationOfWarranty: (Optional[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]): The duration of the warranty promise. Common unitCode values are ANN for year, MON for months, or DAY for days.
    """

    warrantyScope: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    durationOfWarranty: NotRequired[Union[List[Union[SchemaOrgObj, str]], SchemaOrgObj, str]]
    

#WarrantyPromiseInheritedPropertiesTd = WarrantyPromiseInheritedProperties()
#WarrantyPromisePropertiesTd = WarrantyPromiseProperties()


class AllProperties(WarrantyPromiseInheritedProperties , WarrantyPromiseProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[WarrantyPromiseProperties, WarrantyPromiseInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "WarrantyPromise"
    return model
    

WarrantyPromise = create_schema_org_model()