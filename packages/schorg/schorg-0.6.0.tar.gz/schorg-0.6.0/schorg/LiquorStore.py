"""
A shop that sells alcoholic drinks such as wine, beer, whisky and other spirits.

https://schema.org/LiquorStore
"""

from typing import *
from typing_extensions import TypedDict, NotRequired
from pydantic import *
from datetime import *
from time import *


from schorg.schema_org_obj import SchemaOrgObj, SchemaOrgBase


class LiquorStoreInheritedProperties(TypedDict):
    """A shop that sells alcoholic drinks such as wine, beer, whisky and other spirits.

    References:
        https://schema.org/LiquorStore
    Note:
        Model Depth 5
    Attributes:
    """

    


class LiquorStoreProperties(TypedDict):
    """A shop that sells alcoholic drinks such as wine, beer, whisky and other spirits.

    References:
        https://schema.org/LiquorStore
    Note:
        Model Depth 5
    Attributes:
    """

    

#LiquorStoreInheritedPropertiesTd = LiquorStoreInheritedProperties()
#LiquorStorePropertiesTd = LiquorStoreProperties()


class AllProperties(LiquorStoreInheritedProperties , LiquorStoreProperties, TypedDict):
    pass


def create_schema_org_model(type_: Union[LiquorStoreProperties, LiquorStoreInheritedProperties, AllProperties] = AllProperties) -> Type[SchemaOrgBase]:
    model = create_model_from_typeddict(type_, __base__=SchemaOrgBase)
    model.__name__ = "LiquorStore"
    return model
    

LiquorStore = create_schema_org_model()