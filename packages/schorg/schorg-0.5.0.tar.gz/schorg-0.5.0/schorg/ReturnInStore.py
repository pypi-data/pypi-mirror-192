"""
Specifies that product returns must be made in a store.

https://schema.org/ReturnInStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class ReturnInStoreInheritedProperties(TypedDict):
    """Specifies that product returns must be made in a store.

    References:
        https://schema.org/ReturnInStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class ReturnInStoreProperties(TypedDict):
    """Specifies that product returns must be made in a store.

    References:
        https://schema.org/ReturnInStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#ReturnInStoreInheritedPropertiesTd = ReturnInStoreInheritedProperties()
#ReturnInStorePropertiesTd = ReturnInStoreProperties()


class AllProperties(ReturnInStoreInheritedProperties , ReturnInStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[ReturnInStoreProperties, ReturnInStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "ReturnInStore"
    return model
    

ReturnInStore = create_schema_org_model()